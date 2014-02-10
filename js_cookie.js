<script type="text/javascript">
function SetCookie(name, value, Days) { //两个参数，一个是cookie的名子，一个是值
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";
    expires = " + exp.toGMTString() + "; path=/"; //path是cookie的访问路径
}
//取cookies函数  
function getCookie(name) {
    var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
    if (arr != null) 
        return unescape(arr[2]);
    else 
        return null;
}
//删除cookie
function deleteCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null) 
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}
</script>
