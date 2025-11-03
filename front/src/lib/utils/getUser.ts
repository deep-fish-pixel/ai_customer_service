import type {User} from "../types/user";

let userinfo: User = {
    username: '',
    password: '',
    nickname: '',
    user_id: '',
    token: '',
    token_type: '',
}

export function setUser(user: User) {
    userinfo = user;
}

export function getUser() {
    return userinfo;
}

export function getUserId() {
    return userinfo.user_id;
}