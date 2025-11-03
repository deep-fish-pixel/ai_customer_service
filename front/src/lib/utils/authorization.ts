import {getUser} from "./getUser";


export  function getTokenAuthorization() {
    const user = getUser();

    return {
        'Authorization': `${user.token_type} ${user.token}`
    };
}