export class Utils {
    static BASE_URL = "" // add backend url if any
    static PASSWORD_HASH = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4" // add hashed and hexdigest password string here
    static IMG_PATH = "./public/img/" //relative to root directory
    static EXT = '.png'
    static ENDPOINTS = {
        candidates: `${Utils.BASE_URL}/getcandidates`,
        token: `${Utils.BASE_URL}/gettoken`,
        voteapp: `${Utils.BASE_URL}/voteapp`,
        subtmitvotes: `${Utils.BASE_URL}/submitvotes`
    }

    static async sha256(message: string) {
        //bad of js to not have a default hashing library or function
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
    static normalize(str: String) {
        return (str.charAt(0).toUpperCase() + str.substring(1)).replace('_', ' ');
    }
}

export function getObjArrayFromFormData(e: FormData): Object[] {
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

    let arr: Object[] = []
    e.forEach((name, post) => { // value, key instead of key, value
        arr.push({
            "name": name,
            "post": post
        })
    })
    return arr
}
