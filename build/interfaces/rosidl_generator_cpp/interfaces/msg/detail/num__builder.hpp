// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Num.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "interfaces/msg/num.hpp"


#ifndef INTERFACES__MSG__DETAIL__NUM__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__NUM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/num__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Num_finished
{
public:
  explicit Init_Num_finished(::interfaces::msg::Num & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Num finished(::interfaces::msg::Num::_finished_type arg)
  {
    msg_.finished = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Num msg_;
};

class Init_Num_num
{
public:
  Init_Num_num()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Num_finished num(::interfaces::msg::Num::_num_type arg)
  {
    msg_.num = std::move(arg);
    return Init_Num_finished(msg_);
  }

private:
  ::interfaces::msg::Num msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Num>()
{
  return interfaces::msg::builder::Init_Num_num();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__NUM__BUILDER_HPP_
