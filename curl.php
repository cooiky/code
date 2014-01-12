function curl($url) {
  $useragent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1612.1 Safari/537.36';
  $header = array(
"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
//"Accept-Encoding: gzip,deflate,sdch",
"Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
"Cache-Control: max-age=0",
"Connection: keep-alive",
"Host: www.ttmeiju.com"
);
$curl = curl_init(); 
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_HEADER, 0); #head信息不返回
curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
curl_setopt($curl, CURLOPT_USERAGENT, $useragent);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl, CURLOPT_TIMEOUT, 30);
$data = curl_exec($curl);
		
$info = curl_getinfo($curl);
var_dump($info);
if (301 === $info["http_code"]) { #301重定向
curl_close($curl);
return iconv('gbk', 'UTF-8', $info["redirect_url"]); #编码转换
}

if (empty($data)) {
return NULL;
} else {
if (curl_getinfo($curl, CURLINFO_HTTP_CODE) === 200)
return $data;
}
curl_close($curl);

return NULL;
}
