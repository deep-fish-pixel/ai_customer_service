// 用户登录接口
export interface UserLoginRequest {
  username: string;
  password: string;
}

// 用户注册请求参数
export interface UserRegisterRequest extends UserLoginRequest{
  nickname: string;
}

// 用户信息
export interface User extends UserRegisterRequest{
  id: string;
}
