import type {User} from "../types/user";

export const userState = $state(getDefaultUser());

function getDefaultUser(): User {
  return {
    username: '',
    password: '',
    nickname: '',
    user_id: '',
    token: '',
    token_type: '',
  }
}

export function setUser(user: User) {
  Object.assign(userState, user);
  window.localStorage.setItem('user', JSON.stringify(user));
}

export function getUser() {
  if(userState.token){
    return userState;
  }

  const userString = window.localStorage.getItem('user');

  if(userString){
    const user = JSON.parse(userString);
    if(user && user.token){
      return Object.assign(userState, user);
    }
  }

  return userState;
}

export function getUserId() {
  return getUser().username;
}

export function resetUser() {
  Object.assign(userState, getDefaultUser());
  window.localStorage.setItem('user', JSON.stringify(userState));
}