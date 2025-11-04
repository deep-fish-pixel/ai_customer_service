import type {User} from "../types/user";


function getDefaultUser() {
    return {
        username: '',
        password: '',
        nickname: '',
        user_id: '',
        token: '',
        token_type: '',
    }
}
let userinfo: User = getDefaultUser();

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
    return getUser().username;
}

export function resetUser() {
    Object.assign(userinfo, getDefaultUser());
    window.localStorage.setItem('user', JSON.stringify(userinfo));
}