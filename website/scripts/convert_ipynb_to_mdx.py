# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import re
import shutil
import uuid
import warnings
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import mdformat  # @manual=fbsource//third-party/pypi/mdformat:mdformat
import nbformat
import pandas as pd
from lxml import etree  # pyre-ignore
from nbformat.notebooknode import NotebookNode

try:
    from libfb.py.fbcode_root import get_fbcode_dir  # pyre-ignore
except ImportError:
    SCRIPTS_DIR = Path(__file__).parent.resolve()
    LIB_DIR = SCRIPTS_DIR.parent.parent.resolve()
else:
    LIB_DIR = (Path(get_fbcode_dir()) / "beanmachine").resolve()

WEBSITE_DIR = LIB_DIR.joinpath("website")
DOCS_DIR = LIB_DIR.joinpath("docs")
OVERVIEW_DIR = DOCS_DIR.joinpath("overview")
TUTORIALS_DIR = OVERVIEW_DIR.joinpath("tutorials")
# Data display priority. Below lists the priority for displaying data from cell outputs.
# Cells can output many different items, and some will output a fallback display, e.g.
# text/plain if text/html is not working. The below priorities help ensure the output in
# the MDX file shows the best representation of the cell output.
priorities = [
    "text/markdown",
    "image/png",  # matplotlib output.
    "application/vnd.jupyter.widget-view+json",  # tqdm progress bars.
    "application/vnd.bokehjs_load.v0+json",  # Bokeh loading output.
    "application/vnd.bokehjs_exec.v0+json",  # Bokeh `show` outputs.
    "application/vnd.plotly.v1+json",  # Plotly
    "text/html",
    "stream",
    "text/plain",
]


def load_nb_metadata() -> Dict[str, Dict[str, str]]:
    """
    Load the metadata and list of notebooks that are to be converted to MDX.

    Args:
        None

    Returns:
        Dict[str, Dict[str, str]]: A dictionary of metadata needed to convert notebooks
            to MDX. Only those notebooks that are listed in the `tutorials.json` file
            will be included in the Docusaurus MDX output.
    """
    tutorials_json_path = WEBSITE_DIR.joinpath("tutorials.json")
    with tutorials_json_path.open("r") as f:
        tutorials_data = json.load(f)
    return tutorials_data


def load_notebook(path: Path) -> NotebookNode:
    """
    Load the given notebook into memory.

    Args:
        path (Path): Path to the Jupyter notebook.

    Returns:
        NotebookNode: `nbformat` object, which contains all the notebook cells in it.
    """
    with path.open("r") as f:
        nb_str = f.read()
        nb = nbformat.reads(nb_str, nbformat.NO_CONVERT)
    return nb


def create_folders(path: Path) -> Tuple[str, Path]:
    """
    Create asset folders for the tutorial.

    Args:
        path (Path): Path to the Jupyter notebook.

    Returns:
        Tuple[str, Path]: Returns a tuple with the filename to use for the MDX file
            and the path for the MDX assets folder.
    """
    tutorial_folder_name = path.stem
    filename = "".join([token.title() for token in tutorial_folder_name.split("_")])
    tutorial_folder = TUTORIALS_DIR.joinpath(tutorial_folder_name)
    assets_folder = tutorial_folder / "assets"
    img_folder = assets_folder / "img"
    plot_data_folder = assets_folder / "plot_data"
    if not tutorial_folder.exists():
        tutorial_folder.mkdir(parents=True, exist_ok=True)
    if not img_folder.exists():
        img_folder.mkdir(parents=True, exist_ok=True)
    if not plot_data_folder.exists():
        plot_data_folder.mkdir(parents=True, exist_ok=True)
    return filename, assets_folder


def create_frontmatter(path: Path, nb_metadata: Dict[str, Dict[str, str]]) -> str:
    """
    Create frontmatter for the resulting MDX file.

    The frontmatter is the data between the `---` lines in an MDX file.

    Args:
        path (Path): Path to the Jupyter notebook.
        nb_metadata (Dict[str, Dict[str, str]]): The metadata associated with the given
            notebook. Metadata is defined in the `tutorials.json` file.

    Returns:
        str: MDX formatted frontmatter.
    """
    # Add the frontmatter to the MDX string. This is the part between the `---` lines
    # that define the tutorial sidebar_label information.
    frontmatter_delimiter = ["---"]
    frontmatter = [
        f"{key}: {value}"
        for key, value in nb_metadata.get(
            path.stem,
            {
                "title": "",
                "sidebar_label": "",
                "path": "",
                "nb_path": "",
                "github": "",
                "colab": "",
            },
        ).items()
    ]
    frontmatter = "\n".join(frontmatter_delimiter + frontmatter + frontmatter_delimiter)
    mdx = mdformat.text(frontmatter, options={"wrap": 88}, extensions={"myst"})
    return f"{mdx}\n"


def create_imports() -> str:
    """
    Create the imports needed for displaying buttons, and interactive plots in MDX.

    Returns:
        str: MDX formatted imports.
    """
    link_btn = "../../../../website/src/components/LinkButtons.jsx"
    cell_out = "../../../../website/src/components/CellOutput.jsx"
    plot_out = "../../../../website/src/components/Plotting.jsx"
    imports = f'import LinkButtons from "{link_btn}";\n'
    imports += f'import CellOutput from "{cell_out}";\n'
    imports += f'import {{BokehFigure, PlotlyFigure}} from "{plot_out}";\n'
    return f"{imports}\n"


def create_buttons(
    nb_metadata: Dict[str, Dict[str, str]],
    tutorial_folder_name: str,
) -> str:
    """
    Create buttons that link to Colab and GitHub for the tutorial.

    Args:
        nb_metadata (Dict[str, Dict[str, str]]): Metadata for the tutorial.
        tutorial_folder_name (str): The name of the tutorial folder where the MDX
            converted files exist. This is typically just the name of the Jupyter
            notebook file.

    Returns:
        str: MDX formatted buttons.
    """
    github_url = nb_metadata[tutorial_folder_name]["github"]
    colab_url = nb_metadata[tutorial_folder_name]["colab"]
    return f'<LinkButtons\n  githubUrl="{github_url}"\n  colabUrl="{colab_url}"\n/>\n\n'


def handle_images_found_in_markdown(
    markdown: str,
    new_img_dir: Path,
    lib_dir: Path,
) -> str:
    """
    Update image paths in the Markdown, and copy the image to the docs location.

    The pattern we search for in the Markdown is
    ``![alt-text](path/to/image.png "title")`` with two groups:

    - group 1 = path/to/image.png
    - group 2 = "title"

    The first group (the path to the image from the original notebook) will be replaced
    with ``assets/img/{name}`` where the name is `image.png` from the example above. The
    original image will also be copied to the new location
    ``{new_img_dir}/assets/img/{name}``, which can be directly read into the MDX file.

    Args:
        markdown (str): Markdown where we look for Markdown flavored images.
        new_img_dir (Path): Path where images are copied to for display in the
            MDX file.
        lib_dir (Path): The location for the Bean Machine repo.

    Returns:
        str: The original Markdown with new paths for images.
    """
    markdown_image_pattern = re.compile(r"""!\[[^\]]*\]\((.*?)(?=\"|\))(\".*\")?\)""")
    searches = list(re.finditer(markdown_image_pattern, markdown))

    # Return the given Markdown if no images are found.
    if not searches:
        return markdown

    # Convert the given Markdown to a list so we can delete the old path with the new
    # standard path.
    markdown_list = list(markdown)
    for search in searches:
        # Find the old image path and replace it with the new one.
        old_path, _ = search.groups()
        start = 0
        end = 0
        search = re.search(old_path, markdown)
        if search is not None:
            start, end = search.span()
        old_path = Path(old_path)
        name = old_path.name.strip()
        new_path = f"assets/img/{name}"
        del markdown_list[start:end]
        markdown_list.insert(start, new_path)

        # Copy the original image to the new location.
        if old_path.exists():
            old_img_path = old_path
        else:
            # Here we assume the original image exists in the same directory as the
            # notebook, which should be in the tutorials folder of the library.
            old_img_path = (lib_dir / "tutorials" / old_path).resolve()
        new_img_path = str(new_img_dir / name)
        shutil.copy(str(old_img_path), new_img_path)

    return "".join(markdown_list)


def transform_style_attributes(markdown: str) -> str:
    """
    Convert HTML style attributes to something React can consume.

    Args:
        markdown (str): Markdown where we look for HTML style attributes.

    Returns:
        str: The original Markdown with new React style attributes.
    """
    # Finds all instances of `style="attr: value; ..."`.
    token = "style="
    pattern = re.compile(f"""{token}["'`]([^"]*)["'`]""")
    found_patterns = re.findall(pattern, markdown)
    if not found_patterns:
        return markdown

    for found_pattern in found_patterns:
        # Step 1: splits "attr: value; ..." to
        #                ["attr: value", ..."].
        step1 = [token.strip() for token in found_pattern.split(";") if token]

        # Step 2: splits ["attr: value", ...] to
        #                [["attr", "value"], ...].
        step2 = [[token.strip() for token in tokens.split(":")] for tokens in step1]

        # Step 3: converts [["attr", "value"], ...] to
        #                  '{"attr": "value", ...}'.
        step3 = json.dumps(dict(step2))

        # Step 4 wraps the JSON object in {}, so we end up with a string of the form;
        #        '{{"attr": "value", ...}}'.
        step4 = f"{{{step3}}}"

        # Step 5 replaces the old style data with the React style data, and clean the
        #        string for inclusion in the final Markdown.
        markdown = markdown.replace(found_pattern, step4)
        markdown = markdown.replace('"{{', "{{").replace('}}"', "}}")
    return markdown


def handle_markdown_cell(
    cell: NotebookNode,
    new_img_dir: Path,
    lib_dir: Path,
) -> str:
    """
    Handle the given Jupyter Markdown cell and convert it to MDX.

    Args:
        cell (NotebookNode): Jupyter Markdown cell object.
        new_img_dir (Path): Path where images are copied to for display in the
            Markdown cell.
        lib_dir (Path): The location for the Bean Machine library.

    Returns:
        str: Transformed Markdown object suitable for inclusion in MDX.
    """
    markdown = cell["source"]

    # Update image paths in the Markdown and copy them to the Markdown tutorials folder.
    markdown = handle_images_found_in_markdown(markdown, new_img_dir, lib_dir)

    # We will attempt to handle inline style attributes written in HTML by converting
    # them to something React can consume.
    markdown = transform_style_attributes(markdown)

    # Remove any HTML comments from the Markdown. They are fine to keep in the
    # notebooks, but are not really useful in the MDX.
    markdown = re.sub("(<!--.*?-->)", "", markdown, flags=re.DOTALL)
    mdx = mdformat.text(markdown, options={"wrap": 88}, extensions={"myst"})
    return f"{mdx}\n"


def handle_cell_input(cell: NotebookNode, language: str) -> str:
    """
    Create a Markdown cell block using the given cell source, and the language.

    The given language will determine cell input syntax styles. Docusaurus uses Prism as
    the syntax highlighter, https://prismjs.com. See the Docusaurus documentation for
    more information on code blocks
    https://docusaurus.io/docs/markdown-features/code-blocks.

    Args:
        cell (NotebookNode): A notebook cell.
        language (str): Language specifier for syntax highlighting.

    Returns:
        str: Code block formatted Markdown string.
    """
    cell_source = cell.get("source", "")
    return f"```{language}\n{cell_source}\n```\n\n"


def transform_bokeh_json(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform Bokeh JSON found in a cell output to something BokehJS can consume.

    Args:
        json_data (Dict[str, Any]): JSON data found in a notebook's cell output that is
            for Bokeh.

    Returns:
        Dict[str, Any]: Reorganized JSON output for BokehJS.
    """
    key = list(json_data.keys())[0]
    data = json_data[key]
    json_tx = {}
    json_tx["target_id"] = key
    json_tx["root_id"] = data["roots"]["root_ids"][0]
    json_tx["doc"] = {
        "defs": data["defs"],
        "roots": data["roots"],
        "title": data["title"],
        "version": data["version"],
    }
    json_tx["version"] = data["version"]
    return json_tx


def handle_bokeh(
    values: List[Dict[str, Union[int, str, NotebookNode]]],
    plot_data_folder: Path,
) -> List[Tuple[int, str]]:
    """
    Convert Bokeh `show` outputs and Applications to MDX.

    Args:
        values (List[Dict[str, Union[int, str, NotebookNode]]]): Bokeh tagged cell
            outputs.
        plot_data_folder (Path): Path to the folder where plot data should be
            stored.

    Returns:
        List[Tuple[int, str]]: A list of tuples, where the first entry in the tuple is
            the index where the output occurred from the cell, and the second entry of
            the tuple is the MDX formatted string.
    """
    output = []
    for value in values:
        index = int(value["index"])
        data = str(value["data"])
        app_flag = data.startswith("<!DOCTYPE html>")
        json_data = {}
        # Handle Bokeh `show` outputs.
        if not app_flag:
            # Parse the JavaScript for the Bokeh JSON data. The BokehJS output is
            # standardized, so we can make the following assumption for finding the
            # right spot to for the JSON data. Also, this is pure JavaScript so
            # parsing it with lxml is not an option.
            json_string = list(
                filter(
                    lambda line: line.startswith("const docs_json = "),
                    [line.strip() for line in data.splitlines() if line],
                ),
            )[0]

            # Ignore the `const` definition and the ending `;` from the line.
            json_string = json_string[len("const docs_json = ") : -1]
            json_data = json.loads(json_string)

        # Handle Bokeh Applications.
        if app_flag:
            # Bokeh Application objects are rendered in the notebook as HTML. This
            # HTML is saved in the output cell, which we parse below using lxml and
            # xpaths.
            doc = etree.HTML(data)  # pyre-ignore
            scripts = doc.xpath("//body/script[@type='application/json']")
            script = scripts[0]
            script = "".join(script.itertext())
            # Unescape characters. If we skip this step, then the JSON read in by
            # the React BokehFigure object will error in the browser.
            script = script.replace("&amp;", "&")
            script = script.replace("&lt;", "<")
            script = script.replace("&gt;", ">")
            script = script.replace("&quot;", '"')
            script = script.replace("&#x27;", "'")
            script = script.replace("&#x60;", "`")
            json_data = json.loads(script)

        # Shuffle the data so we can save it in a format BokehJS will be able to
        # consume later.
        js = transform_bokeh_json(json_data)
        file_name = js["target_id"]
        # Save the Bokeh JSON data to disk. It will be read by React when loaded in
        # Docusaurus.
        file_path = plot_data_folder / f"{file_name}.json"
        with file_path.open("w") as f:
            json.dump(js, f, indent=2)

        # Add the Bokeh figure to the MDX output.
        path_to_data = f"./assets/plot_data/{file_name}.json"
        output.append(
            (index, f"<BokehFigure data={{require('{path_to_data}')}} />\n\n"),
        )
    return output


def handle_image(
    values: List[Dict[str, Union[int, str, NotebookNode]]],
) -> List[Tuple[int, str]]:
    """
    Convert embedded images to string MDX can consume.

    Args:
        values (List[Dict[str, Union[int, str, NotebookNode]]]): Bokeh tagged cell
            outputs.

    Returns:
        List[Tuple[int, str]]: A list of tuples, where the first entry in the tuple is
            the index where the output occurred from the cell, and the second entry of
            the tuple is the MDX formatted string.
    """
    output = []
    for value in values:
        index = value["index"]
        mime_type = value["mime_type"]
        img = value["data"]
        output.append((index, f"![](data:image/{mime_type};base64,{img})\n\n"))
    return output


def handle_markdown(
    values: List[Dict[str, Union[int, str, NotebookNode]]],
) -> List[Tuple[int, str]]:
    """
    Convert and format Markdown for MDX.

    Args:
        values (List[Dict[str, Union[int, str, NotebookNode]]]): Bokeh tagged cell
            outputs.

    Returns:
        List[Tuple[int, str]]: A list of tuples, where the first entry in the tuple is
            the index where the output occurred from the cell, and the second entry of
            the tuple is the MDX formatted string.
    """
    output = []
    for value in values:
        index = int(value["index"])
        markdown = str(value["data"])
        markdown = mdformat.text(markdown, options={"wrap": 88}, extensions={"myst"})
        output.append((index, f"{markdown}\n\n"))
    return output


def handle_pandas(
    values: List[Dict[str, Union[int, str, NotebookNode]]],
) -> List[Tuple[int, str]]:
    """
    Handle how to display pandas DataFrames.

    There is a scoped style tag in the DataFrame output that uses the class name
    `dataframe` to style the output. We will use this token to determine if a pandas
    DataFrame is being displayed.

    Args:
        values (List[Dict[str, Union[int, str, NotebookNode]]]): Bokeh tagged cell
            outputs.

    Returns:
        List[Tuple[int, str]]: A list of tuples, where the first entry in the tuple is
            the index where the output occurred from the cell, and the second entry of
            the tuple is the MDX formatted string.
    """
    output = []
    for value in values:
        index = int(value["index"])
        data = str(value["data"])
        df = pd.read_html(data, flavor="lxml")
        # NOTE: The return is a list of dataframes and we only care about the first
        #       one.
        md_df = df[0]
        for column in md_df.columns:
            if column.startswith("Unnamed"):
                md_df.rename(columns={column: ""}, inplace=True)
        # Remove the index if it is just a range, and output to markdown.
        mdx = ""
        if isinstance(md_df.index, pd.RangeIndex):
            # Ignore FutureWarning: 'showindex' is deprecated.
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=FutureWarning)
                mdx = md_df.to_markdown(showindex=False)
        elif not isinstance(md_df.index, pd.RangeIndex):
            mdx = md_df.to_markdown()
        output.append((index, f"\n{mdx}\n\n"))
    return output


def handle_plain(
    values: List[Dict[str, Union[int, str, NotebookNode]]],
) -> List[Tuple[int, str]]:
    """
    Handle how to plain cell output should be displayed in MDX.

    Args:
        values (List[Dict[str, Union[int, str, NotebookNode]]]): Bokeh tagged cell
            outputs.

    Returns:
        List[Tuple[int, str]]: A list of tuples, where the first entry in the tuple is
            the index where the output occurred from the cell, and the second entry of
            the tuple is the MDX formatted string.
    """
    output = []
    for value in values:
        index = int(value["index"])
        data = str(value["data"])
        data = [line.strip() for line in data.splitlines() if line]
        data = [datum for datum in data if datum]
        if data:
            data = "\n".join([line for line in str(value["data"]).splitlines() if line])
            output.append(
                (index, f"<CellOutput>\n{{\n  `{data}`\n}}\n</CellOutput>\n\n"),
            )
    return output


def handle_plotly(
    values: List[Dict[str, Union[int, str, NotebookNode]]],
    plot_data_folder: Path,
) -> List[Tuple[int, str]]:
    """
    Convert Plotly outputs to MDX.

    Args:
        values (List[Dict[str, Union[int, str, NotebookNode]]]): Bokeh tagged cell
            outputs.
        plot_data_folder (Path): Path to the folder where plot data should be
            stored.

    Returns:
        List[Tuple[int, str]]: A list of tuples, where the first entry in the tuple is
            the index where the output occurred from the cell, and the second entry of
            the tuple is the MDX formatted string.
    """
    output = []
    for value in values:
        index = value["index"]
        data = value["data"]
        file_name = str(uuid.uuid4())
        file_path = plot_data_folder / f"{file_name}.json"
        path_to_data = f"./assets/plot_data/{file_name}.json"
        output.append(
            (index, f"<PlotlyFigure data={{require('{path_to_data}')}} />\n\n"),
        )
        with file_path.open("w") as f:
            json.dump(data, f, indent=2)
    return output


def handle_tqdm(
    values: List[Dict[str, Union[int, str, NotebookNode]]],
) -> List[Tuple[int, str]]:
    """
    Handle the output of tqdm.

    tqdm will be displayed as separate CellOutput React components if we do not
    aggregate them all into a single CellOutput object, which is what this method does.

    Args:
        values (List[Dict[str, Union[int, str, NotebookNode]]]): Bokeh tagged cell
            outputs.

    Returns:
        List[Tuple[int, str]]: A list of tuples, where the first entry in the tuple is
            the index where the output occurred from the cell, and the second entry of
            the tuple is the MDX formatted string.
    """
    output = sorted(values, key=lambda item: item["index"])
    index = int(output[0]["index"])
    md = "\n".join([str(item["data"]) for item in output if item["data"]])
    return [(index, f"<CellOutput>\n{{\n  `{md}`\n}}\n</CellOutput>\n\n")]


CELL_OUTPUTS_TO_PROCESS = Dict[
    str,
    List[Dict[str, Union[int, str, NotebookNode]]],
]


def aggregate_mdx(
    cell_outputs_to_process: CELL_OUTPUTS_TO_PROCESS,
    plot_data_folder: Path,
) -> str:
    """
    Aggregate the `cell_outputs_to_process` into MDX.

    Args:
        cell_outputs_to_process (CELL_OUTPUTS_TO_PROCESS): A dictionary of cell outputs
            that need further processing.
        plot_data_folder (Path): Path to where plot data should be stored for the
            tutorial.

    Returns:
        str: MDX formatted string.
    """
    processed_mdx = []
    for key, values in cell_outputs_to_process.items():
        if not values:
            continue
        if key == "bokeh":
            processed_mdx.extend(handle_bokeh(values, plot_data_folder))
        if key == "image":
            processed_mdx.extend(handle_image(values))
        if key == "markdown":
            processed_mdx.extend(handle_markdown(values))
        if key == "pandas":
            processed_mdx.extend(handle_pandas(values))
        if key == "plain":
            processed_mdx.extend(handle_plain(values))
        if key == "plotly":
            processed_mdx.extend(handle_plotly(values, plot_data_folder))
        if key == "tqdm":
            processed_mdx.extend(handle_tqdm(values))

    # Ensure the same ordering of the MDX happens as was found in the original cell
    # output.
    processed_mdx = sorted(processed_mdx, key=lambda item: item[0])
    mdx = "\n".join([item[1] for item in processed_mdx])
    return mdx


def prioritize_dtypes(
    cell_outputs: List[NotebookNode],
) -> Tuple[List[List[str]], List[bool]]:
    """
    Prioritize cell output data types.

    Args:
        cell_outputs (List[NotebookNode]): A list of cell outputs.

    Returns:
        Tuple[List[List[str]], List[bool]]: Return two items in the tuple; the first is
            a list of prioritized data types and the second is a list boolean values
            associated with the cell output having Plotly information in it or not.
    """
    cell_output_dtypes = [
        list(cell_output["data"].keys())
        if "data" in cell_output
        else [cell_output["output_type"]]
        for cell_output in cell_outputs
    ]
    prioritized_cell_output_dtypes = [
        sorted(
            set(dtypes).intersection(set(priorities)),
            key=lambda dtype: priorities.index(dtype),
        )
        for dtypes in cell_output_dtypes
    ]
    prioritized_cell_output_dtypes = [
        [str(item) for item in items] for items in prioritized_cell_output_dtypes
    ]
    plotly_flags = [
        any(["plotly" in output for output in outputs])
        for outputs in cell_output_dtypes
    ]
    return prioritized_cell_output_dtypes, plotly_flags


def aggregate_bokeh(
    prioritized_data_dtype: str,
    cell_output: NotebookNode,
    data: NotebookNode,
    cell_outputs_to_process: CELL_OUTPUTS_TO_PROCESS,
    i: int,
) -> None:
    """
    Aggregate Bokeh cell outputs.

    Args:
        prioritized_data_dtype (str): The prioritized cell output data type.
        cell_output (NotebookNode): The actual cell output from the notebook.
        data (NotebookNode): The data of the cell output.
        cell_outputs_to_process (CELL_OUTPUTS_TO_PROCESS): Dictionary containing
            aggregated cell output objects.
        i (int): Index for the cell output in the list of cell output objects.

    Returns:
        None: Does not return anything, instead adds values to the
            cell_outputs_to_process if applicable.
    """
    if prioritized_data_dtype == "application/vnd.bokehjs_load.v0+json":
        pass
    # Bokeh `show` outputs.
    if prioritized_data_dtype == "application/vnd.bokehjs_exec.v0+json":
        data = cell_output["data"]["application/javascript"]
        cell_outputs_to_process["bokeh"].append({"index": i, "data": data})
    # Bokeh applications.
    if prioritized_data_dtype == "text/html" and "Bokeh Application" in data:
        cell_outputs_to_process["bokeh"].append({"index": i, "data": data})


def aggregate_images_and_plotly(
    prioritized_data_dtype: str,
    cell_output: NotebookNode,
    data: NotebookNode,
    plotly_flags: List[bool],
    cell_outputs_to_process: CELL_OUTPUTS_TO_PROCESS,
    i: int,
) -> None:
    """
    Aggregates images or Plotly cell outputs into an appropriate bucket.

    Args:
        prioritized_data_dtype (str): The prioritized cell output data type.
        cell_output (NotebookNode): The actual cell output from the notebook.
        data (NotebookNode): The data of the cell output.
        plotly_flags (List[bool]): True if a Plotly plot was found in the cell outputs
            else False.
        cell_outputs_to_process (CELL_OUTPUTS_TO_PROCESS): Dictionary containing
            aggregated cell output objects.
        i (int): Index for the cell output in the list of cell output objects.

    Returns:
        None: Does not return anything, instead adds values to the
            cell_outputs_to_process if applicable.
    """
    if prioritized_data_dtype.startswith("image"):
        if not plotly_flags[i]:
            cell_outputs_to_process["image"].append(
                {"index": i, "data": data, "mime_type": prioritized_data_dtype},
            )
        # Plotly outputs a static image, but we can use the JSON in the cell
        # output to create interactive plots using a React component.
        if plotly_flags[i]:
            data = cell_output["data"]["application/vnd.plotly.v1+json"]
            cell_outputs_to_process["plotly"].append({"index": i, "data": data})


def aggregate_plain_output(
    prioritized_data_dtype: str,
    cell_output: NotebookNode,
    data: NotebookNode,
    cell_outputs_to_process: CELL_OUTPUTS_TO_PROCESS,
    i: int,
) -> None:
    """
    Aggregate plain text cell outputs together.

    Args:
        prioritized_data_dtype (str): The prioritized cell output data type.
        cell_output (NotebookNode): The actual cell output from the notebook.
        data (NotebookNode): The data of the cell output.
        cell_outputs_to_process (CELL_OUTPUTS_TO_PROCESS): Dictionary containing
            aggregated cell output objects.
        i (int): Index for the cell output in the list of cell output objects.

    Returns:
        None: Does not return anything, instead adds values to the
            cell_outputs_to_process if applicable.
    """
    # Ignore error outputs.
    if "name" in cell_output and cell_output["name"] == "stderr":
        pass
    # Ignore matplotlib legend text output.
    if prioritized_data_dtype == "text/plain" and "matplotlib" in data:
        pass
    cell_outputs_to_process["plain"].append({"index": i, "data": data})


def aggregate_output_types(cell_outputs: List[NotebookNode]) -> CELL_OUTPUTS_TO_PROCESS:
    """
    Aggregate cell outputs into a dictionary for further processing.

    Args:
        cell_outputs (List[NotebookNode]): List of cell outputs.

    Returns:
        CELL_OUTPUTS_TO_PROCESS: Dictionary containing aggregated cell output objects.
    """
    # We will use the below cell output data types for prioritizing the output shown in
    # the MDX file.
    prioritized_cell_output_dtypes, plotly_flags = prioritize_dtypes(cell_outputs)

    cell_outputs_to_process = {
        "bokeh": [],
        "image": [],
        "markdown": [],
        "pandas": [],
        "plain": [],
        "plotly": [],
        "tqdm": [],
    }
    for i, cell_output in enumerate(cell_outputs):
        prioritized_data_dtype = prioritized_cell_output_dtypes[i][0]

        # If there is no `data` key in the cell_output, then it may be an error that
        # needs to be handled. Even if it is not an error, the data is stored in a
        # different key if no `data` key is found.
        data = (
            cell_output["data"][prioritized_data_dtype]
            if "data" in cell_output
            else cell_output["text"]
        )
        bokeh_check = "bokeh" in prioritized_data_dtype or (
            prioritized_data_dtype == "text/html" and "Bokeh Application" in data
        )
        if bokeh_check:
            aggregate_bokeh(
                prioritized_data_dtype,
                cell_output,
                data,
                cell_outputs_to_process,
                i,
            )
        image_check = prioritized_data_dtype.startswith("image")
        if image_check:
            aggregate_images_and_plotly(
                prioritized_data_dtype,
                cell_output,
                data,
                plotly_flags,
                cell_outputs_to_process,
                i,
            )
        plain_check = prioritized_data_dtype in ["text/plain", "stream"]
        if plain_check:
            aggregate_plain_output(
                prioritized_data_dtype,
                cell_output,
                data,
                cell_outputs_to_process,
                i,
            )
        if prioritized_data_dtype == "text/markdown":
            cell_outputs_to_process["markdown"].append({"index": i, "data": data})
        if "dataframe" in data:
            cell_outputs_to_process["pandas"].append({"index": i, "data": data})
        if prioritized_data_dtype == "application/vnd.jupyter.widget-view+json":
            data = cell_output["data"]["text/plain"]
            cell_outputs_to_process["tqdm"].append({"index": i, "data": data})

    return cell_outputs_to_process


def handle_cell_outputs(cell: NotebookNode, plot_data_folder: Path) -> str:
    """
    Handle cell outputs and convert to MDX.

    Args:
        cell (NotebookNode): The cell where the outputs need converting.
        plot_data_folder (Path): Path to the folder where plot data should be
            stored.

    Returns:
        str: MDX formatted cell output.
    """
    mdx = ""

    # Return an empty string if there are no actual cell outputs.
    cell_outputs = cell.get("outputs", [])
    if not cell_outputs:
        return mdx

    # We will loop over all cell outputs and bucket them into the appropriate key in the
    # dictionary below for further processing. Doing it in this way helps aggregate like
    # outputs together e.g. tqdm outputs.
    cell_outputs_to_process = aggregate_output_types(cell_outputs)

    # Now we process all aggregated cell outputs into a single output for the type.
    md = aggregate_mdx(cell_outputs_to_process, plot_data_folder)
    return md


def handle_code_cell(cell: NotebookNode, plot_data_folder: Path) -> str:
    """
    Handle code cells in Jupyter notebooks and convert them to MDX.

    Args:
        cell (NotebookNode): A Jupyter notebook cell that contains code.
        plot_data_folder (Path): Path to the folder where plot data should be
            stored.

    Returns:
        str: MDX formatted code cell.
    """
    cell_input_mdx = handle_cell_input(cell, "python")
    cell_output_mdx = handle_cell_outputs(cell, plot_data_folder)
    return cell_input_mdx + cell_output_mdx


def transform_notebook(path: Path) -> str:
    """
    Transform a notebook located at the given path into MDX.

    Args:
        path (Path): Path to the Jupyter notebook tutorial.

    Returns:
        str: MDX formatted string.
    """
    filename, assets_folder = create_folders(path)
    img_folder = assets_folder / "img"
    plot_data_folder = assets_folder / "plot_data"
    save_folder = assets_folder.joinpath("..").resolve()
    nb = load_notebook(path)
    nb_metadata = load_nb_metadata()
    mdx = ""
    mdx += create_frontmatter(path, nb_metadata)
    mdx += create_imports()
    mdx += create_buttons(nb_metadata, path.stem)
    for cell in nb["cells"]:
        cell_type = cell["cell_type"]

        # Handle a Markdown cell.
        if cell_type == "markdown":
            mdx += handle_markdown_cell(cell, img_folder, LIB_DIR)

        # Handle a code cell.
        if cell_type == "code":
            mdx += handle_code_cell(cell, plot_data_folder)

    # Write the MDX file to disk.
    save_path = save_folder / f"{filename}.mdx"
    with save_path.open("w") as f:
        f.write(mdx)

    # Return the string for debugging purposes.
    return mdx


if __name__ == "__main__":
    tutorials_metadata = load_nb_metadata()
    print("--------------------------------------------")
    print("Converting tutorial notebooks into mdx files")
    print("--------------------------------------------")
    for _, value in tutorials_metadata.items():
        path = (LIB_DIR / value["nb_path"]).resolve()
        print(f"{path.stem}")
        mdx = transform_notebook(path)
    print("")
