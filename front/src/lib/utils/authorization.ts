import {getUser} from "../state/userState.svelte";

export  function getTokenAuthorization() {
    const user = getUser();

    return {
        'Authorization': `${user.token_type} ${user.token}`
    };
}