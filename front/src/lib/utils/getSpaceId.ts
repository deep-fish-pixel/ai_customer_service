let loc = window.location;
const spaceRegExp = /^\/space\/(\w+)$/;

export default function () {
    const matches = loc.pathname.match(spaceRegExp);

    if (matches) {
        return matches[1];
    }

    return '';
}