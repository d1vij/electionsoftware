export class Utils {
    static PASSWORD_HASH = "";
    static ENDPOINTS = {
        candidates: `/getcandidates`,
        token: `/gettoken`,
        voteapp: `/voteapp`,
        submitvotes: `/submitvotes`
    };
    static async sha256(message) {
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
    static normalize(str) {
        return (str.charAt(0).toUpperCase() + str.substring(1)).replace('_', ' ');
    }
}
export function getObjArrayFromFormData(e) {
    /*
    converts form data into array of objects of format
    [
        {
          "name": "divij",
          "post": "head_boy"
        },
        {
          "name": "abc",
          "post": "head_girl"
        }
      ]
     */
    let arr = [];
    e.forEach((name, post) => {
        arr.push({
            "name": name,
            "post": post
        });
    });
    return arr;
}
