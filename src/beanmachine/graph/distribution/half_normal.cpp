// Copyright (c) Facebook, Inc. and its affiliates.
#include <cmath>
#include <random>
#include <string>

#include "beanmachine/graph/distribution/half_normal.h"

namespace beanmachine {
namespace distribution {

using namespace graph;

Half_Normal::Half_Normal(
    AtomicType sample_type,
    const std::vector<Node*>& in_nodes)
    : Distribution(DistributionType::HALF_NORMAL, sample_type) {
  // a Half_Normal distribution has one parent
  // sigma -> positive real
  if (in_nodes.size() != 1) {
    throw std::invalid_argument(
        "Half_Normal distribution must have exactly one parent");
  }
  if (in_nodes[0]->value.type != graph::AtomicType::POS_REAL) {
    throw std::invalid_argument(
        "Half_Normal parent must be a positive real number");
  }
  // only real-valued samples are possible
  if (sample_type != AtomicType::REAL) {
    throw std::invalid_argument(
        "Half_Normal distribution produces real number samples");
  }
}

double Half_Normal::_double_sampler(std::mt19937& gen) const {
  std::normal_distribution<double> dist(0.0, in_nodes[0]->value._double);
  return std::abs(dist(gen));
}

// The calculations for the normal distribution. Very helpful for half-normal!
// log_prob of a normal: - log(s) -0.5 log(2*pi) - 0.5 (x - m)^2 / s^2
// grad  w.r.t. value x: - (x - m) / s^2
// grad2 w.r.t. value x: - 1 / s^2
// grad  w.r.t. s : -1/s + (x-m)^2 / s^3
// grad2 w.r.t. s : 1/s^2 - 3 (x-m)^2 / s^4
// grad  w.r.t. m : (x - m) / s^2
// grad2 w.r.t. m : -1 / s^2
// First order chain rule: f(g(x))' = f'(g(x)) g'(x),
// - In backward propagation, f'(g(x)) is given by adjunct, the above equation
// computes g'(x). [g is the current function f is the final target]
// - In forward propagation, g'(x) is given by in_nodes[x]->grad1,
// the above equation computes f'(g) [f is the current function g is the input]

/// TODO[Walid:] The following math needs to be implemented
// log_prob of a half-normal:
//    (x<0)? 0 : log(2) - log(s) -0.5 log(2*pi) - 0.5 (x - m)^2 / s^2
// grad  w.r.t. value x:
//    (x<0)? 0 : - (x - m) / s^2
// grad2 w.r.t. value x:
//    (x<0)? 0 : - 1 / s^2
// grad  w.r.t. s :
//    (x<0)? 0 : -1/s + (x-m)^2 / s^3 grad2 w.r.t. s : 1/s^2 - 3 (x-m)^2 / s^4
// grad  w.r.t. m :
//    (x<0)? 0 : (x - m) / s^2
// grad2 w.r.t. m :
//    (x<0)? 0 : -1 / s^2

/// TODO[Walid]: The following notes are mysterious to me.
// First order chain rule: f(g(x))' = f'(g(x)) g'(x),
// - In backward propagation, f'(g(x)) is given by adjunct, the above equation
// computes g'(x). [g is the current function f is the final target]
// - In forward propagation, g'(x) is given by in_nodes[x]->grad1,
// the above equation computes f'(g) [f is the current function g is the input]

double Half_Normal::log_prob(const NodeValue& value) const {
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double result, sum_x, sum_xsq;
  int size;

  if (value.type.variable_type == graph::VariableType::SCALAR) {
    size = 1;
    sum_x = value._double;
    sum_xsq = value._double * value._double;
  } else if (
      value.type.variable_type == graph::VariableType::BROADCAST_MATRIX) {
    size = value._matrix.size();
    sum_x = value._matrix.sum();
    sum_xsq = value._matrix.squaredNorm();
  } else {
    throw std::runtime_error(
        "Half_Normal::log_prob applied to invalid variable type");
  }
  // This is computing the log probability of the Normal PDF
  // for the entire sample
  /// TODO[Walid]: For half normal we should add (log 2)*size
  /// TODO[Walid]: Should we also add a check on mean?
  result = (-std::log(s) - 0.5 * std::log(2 * M_PI)) * size -
      0.5 * (sum_xsq - 2 * m * sum_x + m * m * size) / (s * s);
  return result;
}

void Half_Normal::log_prob_iid(
    const graph::NodeValue& value,
    Eigen::MatrixXd& log_probs) const {
  assert(value.type.variable_type == graph::VariableType::BROADCAST_MATRIX);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  /// TODO[Walid]: Need to figure out how to do constants and conditionals here
  log_probs = (-std::log(s) - 0.5 * std::log(2 * M_PI)) -
      0.5 * (value._matrix.array() - m).pow(2) / (s * s);
}

/// TODO[Walid]: This function can be inlined (it has only two uses)
/// TODO[Walid]: Will need to be conditioned by x either here or at call site
void Half_Normal::_grad1_log_prob_value(
    double& grad1,
    double val,
    double m,
    double s_sq) {
  grad1 += -(val - m) / s_sq;
};

void Half_Normal::gradient_log_prob_value(
    const NodeValue& value,
    double& grad1,
    double& grad2) const {
  assert(value.type.variable_type == graph::VariableType::SCALAR);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;
  _grad1_log_prob_value(grad1, value._double, m, s_sq);
  grad2 += -1 / s_sq;
}

void Half_Normal::gradient_log_prob_param(
    const NodeValue& value,
    double& grad1,
    double& grad2) const {
  assert(value.type.variable_type == graph::VariableType::SCALAR);
  double x = value._double;
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;
  /// gradients of m should be non-zero before computing gradients w.r.t. m
  /// TODO[Walid]: The above is a peculiar requirement. What's the intention?
  double m_grad = 0.0; /// TODO[Walid]: A bit unsure about just zeroing this out
  double m_grad2 =
      0.0; /// TODO[Walid]: A bit unsure about just zeroing this out
  /// Following conditional should probably also go
  if (m_grad != 0 or m_grad2 != 0) {
    double grad_m = (x - m) / s_sq;
    double grad2_m2 = -1 / s_sq;
    grad1 += grad_m * m_grad;
    grad2 += grad2_m2 * m_grad * m_grad + grad_m * m_grad2;
  }
  double s_grad = in_nodes[0]->grad1;
  double s_grad2 = in_nodes[0]->grad2;
  if (s_grad != 0 or s_grad2 != 0) {
    double grad_s = -1 / s + (x - m) * (x - m) / (s * s * s);
    double grad2_s2 = 1 / s_sq - 3 * (x - m) * (x - m) / (s_sq * s_sq);
    grad1 += grad_s * s_grad;
    grad2 += grad2_s2 * s_grad * s_grad + grad_s * s_grad2;
  }
}

void Half_Normal::backward_value(
    const graph::NodeValue& value,
    graph::DoubleMatrix& back_grad,
    double adjunct) const {
  assert(value.type.variable_type == graph::VariableType::SCALAR);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;
  double increment = 0.0;
  _grad1_log_prob_value(increment, value._double, m, s_sq);
  back_grad._double += adjunct * increment;
}

void Half_Normal::backward_value_iid(
    const graph::NodeValue& value,
    graph::DoubleMatrix& back_grad) const {
  assert(value.type.variable_type == graph::VariableType::BROADCAST_MATRIX);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;
  back_grad._matrix -= ((value._matrix.array() - m) / s_sq).matrix();
}

void Half_Normal::backward_value_iid(
    const graph::NodeValue& value,
    graph::DoubleMatrix& back_grad,
    Eigen::MatrixXd& adjunct) const {
  assert(value.type.variable_type == graph::VariableType::BROADCAST_MATRIX);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;
  back_grad._matrix -=
      (adjunct.array() * (value._matrix.array() - m) / s_sq).matrix();
}

void Half_Normal::backward_param(const graph::NodeValue& value, double adjunct)
    const {
  assert(value.type.variable_type == graph::VariableType::SCALAR);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;
  double jacob_0 = (value._double - m) / s_sq;

  /// Delete the following
  /// if (in_nodes[0]->needs_gradient()) {
  ///  in_nodes[0]->back_grad1._double += adjunct * jacob_0;
  /// }
  if (in_nodes[0]->needs_gradient()) {
    in_nodes[0]->back_grad1._double +=
        adjunct * (-1 / s + jacob_0 * jacob_0 * s);
  }
}

void Half_Normal::backward_param_iid(const graph::NodeValue& value) const {
  assert(value.type.variable_type == graph::VariableType::BROADCAST_MATRIX);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;

  int size = value._matrix.size();
  double sum_x = value._matrix.sum();
  /// The following should be deleted
  ///  if (in_nodes[0]->needs_gradient()) {
  ///    in_nodes[0]->back_grad1._double += sum_x / s_sq - size * m / s_sq;
  ///  }
  if (in_nodes[0]->needs_gradient()) {
    double sum_xsq = value._matrix.squaredNorm();
    in_nodes[0]->back_grad1._double +=
        (-size / s + (sum_xsq - 2 * m * sum_x + m * m * size) / (s * s_sq));
  }
}

void Half_Normal::backward_param_iid(
    const graph::NodeValue& value,
    Eigen::MatrixXd& adjunct) const {
  assert(value.type.variable_type == graph::VariableType::BROADCAST_MATRIX);
  double m = 0.0;
  double s = in_nodes[0]->value._double;
  double s_sq = s * s;

  double sum_x = (value._matrix.array() * adjunct.array()).sum();
  double sum_adjunct = adjunct.sum();
  /// The following should be deleted
  /// if (in_nodes[0]->needs_gradient()) {
  ///  in_nodes[0]->back_grad1._double += sum_x / s_sq - sum_adjunct * m / s_sq;
  /// }
  if (in_nodes[0]->needs_gradient()) {
    double sum_xsq = (value._matrix.array().pow(2) * adjunct.array()).sum();
    in_nodes[0]->back_grad1._double +=
        (-sum_adjunct / s +
         (sum_xsq - 2 * m * sum_x + m * m * sum_adjunct) / (s * s_sq));
  }
}

} // namespace distribution
} // namespace beanmachine