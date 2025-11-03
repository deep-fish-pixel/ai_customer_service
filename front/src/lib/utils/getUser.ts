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
    window.localStorage.setItem('user', JSON.stringify(user));
}

export function getUser() {
    if(userinfo.token){
        return userinfo;
    }

    const userString = window.localStorage.getItem('user');

    if(userString){
        const user = JSON.parse(userString);
        if(user && user.token){
            return userinfo = user;
        }
    }

    return userinfo;
}

export function getUserId() {
    return userinfo.user_id;
}