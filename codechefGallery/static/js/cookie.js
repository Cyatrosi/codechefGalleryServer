// =========== Cookie Functions =======
export function setCookie(data){
    document.cookie = JSON.stringify(data);
}
export function clearCookie(data){
    document.cookie = "";
}
export function getCookie(){
    var cookies = document.cookie.split(";");
    if(cookies.length >1){
        return JSON.parse(cookies[1]);
    }
    return "";
}