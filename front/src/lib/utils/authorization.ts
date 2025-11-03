import {getUser} from "./getUser";


export  function getTokenAuthorization() {
    const user = getUser();

    return {
        'Authorization': `${'Bearer' || user.token_type} ${user.token}`
    };
}