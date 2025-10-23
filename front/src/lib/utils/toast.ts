
let toast = (message: string) =>  undefined;

export function injectToast(newToast: typeof toast) {
    toast = newToast
}

export function showToast(message: string) {
    if (toast) {
        toast(message);
    }
}