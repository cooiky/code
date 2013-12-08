$url = trim($_GET["durl"]);
$jsoncallback = trim($_GET['jsoncallback']);
/**
* 使用BCS云存储，保存处理后的图片(注意：需要用户开启云存储服务)
*/
require_once('BaeImageService.class.php');
require_once("conf.inc.php");
 
/****1. 执行image服务****/
$baeImageTransform = new BaeImageTransform();
//$baeImageTransform->setHue(50);
$baeImageTransform->setQuality(80);

//创建服务功能对象
$baeImageService = new BaeImageService();
$retVal = $baeImageService->applyTransformByObject($url, $baeImageTransform);
 
/****2. 将结果保存到云存储****/
if ($retVal !== false && isset($retVal['response_params']) && isset($retVal['response_params']['image_data'])) {
	$imageSrc = base64_decode($retVal['response_params']['image_data']);
	$bcs_ak = BCS_AK;//填入您申请bcs服务时候的ak和sk
	$bcs_sk = BCS_SK;
	$bcs_host = 'bcs.duapp.com';
	$baiduBCS = new BaiduBCS($bcs_ak, $bcs_sk, $bcs_host);
 
	$bucket = "a720pim";//填入您申请bcs的bucket名称
	$img = preg_split("/\//", $url);
 
	//object name
	$filename = $img[count($img) - 1];//填入您要保存的名称
	$object = '/' . $filename; //object必须以‘/’开头
 
	//将图片存入云存储
	//$imageSrc即为请求image服务成功后返回的图片二进制数据
	$response = $baiduBCS->create_object_by_content($bucket, $object, $imageSrc);
	if (!$response->isOK()){
		die('Create object failed.');
	}
 
	//得到已存入云存储图片的url
	$data['img_url'] = $baiduBCS->generate_get_object_url($bucket, $object);
	if($url === false){
		echo 'Generate GET object url failed.';	
	}
	echo $jsoncallback."(".json_encode($data).")";
} else {
	echo 'transform failed, error:' . $baeImageService->errmsg();
}
