// Copyright (c) Facebook, Inc. and its affiliates.
#include "beanmachine/graph/distribution/bernoulli.h"
#include "beanmachine/graph/distribution/bernoulli_noisy_or.h"
#include "beanmachine/graph/distribution/beta.h"
#include "beanmachine/graph/distribution/binomial.h"
#include "beanmachine/graph/distribution/distribution.h"
#include "beanmachine/graph/distribution/tabular.h"
#include "beanmachine/graph/distribution/flat.h"
#include "beanmachine/graph/distribution/normal.h"
#include "beanmachine/graph/distribution/half_cauchy.h"
#include "beanmachine/graph/distribution/student_t.h"
#include "beanmachine/graph/distribution/bernoulli_logit.h"
#include "beanmachine/graph/distribution/gamma.h"
#include "beanmachine/graph/distribution/bimixture.h"

namespace beanmachine {
namespace distribution {

std::unique_ptr<Distribution> Distribution::new_distribution(
    graph::DistributionType dist_type,
    graph::ValueType sample_type,
    const std::vector<graph::Node*>& in_nodes) {
  // call the appropriate distribution constructor
  if(sample_type.variable_type == graph::VariableType::SCALAR){
    auto atype = sample_type.atomic_type;
    switch(dist_type) {
      case graph::DistributionType::TABULAR: {
        return std::make_unique<Tabular>(atype, in_nodes);
      }
      case graph::DistributionType::BERNOULLI: {
        return std::make_unique<Bernoulli>(atype, in_nodes);
      }
      case graph::DistributionType::BERNOULLI_NOISY_OR: {
        return std::make_unique<BernoulliNoisyOr>(atype, in_nodes);
      }
      case graph::DistributionType::BETA: {
        return std::make_unique<Beta>(atype, in_nodes);
      }
      case graph::DistributionType::BINOMIAL: {
        return std::make_unique<Binomial>(atype, in_nodes);
      }
      case graph::DistributionType::FLAT: {
        return std::make_unique<Flat>(atype, in_nodes);
      }
      case graph::DistributionType::NORMAL: {
        return std::make_unique<Normal>(atype, in_nodes);
      }
      case graph::DistributionType::HALF_CAUCHY: {
        return std::make_unique<HalfCauchy>(atype, in_nodes);
      }
      case graph::DistributionType::STUDENT_T: {
        return std::make_unique<StudentT>(atype, in_nodes);
      }
      case graph::DistributionType::BERNOULLI_LOGIT: {
        return std::make_unique<BernoulliLogit>(atype, in_nodes);
      }
      case graph::DistributionType::GAMMA: {
        return std::make_unique<Gamma>(atype, in_nodes);
      }
      case graph::DistributionType::BIMIXTURE: {
        return std::make_unique<Bimixture>(atype, in_nodes);
      }
      default: {
        throw std::invalid_argument(
            "Unknown distribution " +
            std::to_string(static_cast<int>(dist_type)) +
            " for univariate sample type.");
      }
    }
  }
  switch(dist_type) {
    default: {
      throw std::invalid_argument(
          "Unknown distribution " +
          std::to_string(static_cast<int>(dist_type)) +
          " for multivariate sample type.");
    }
  }
}

} // namespace distribution
} // namespace beanmachine
