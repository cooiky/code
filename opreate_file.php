<?php
function delete($filename) { #$filename 绝对路径
	if (file_exists($filename))
		unlink($filename);
}

function write($str, $filename) { #$filename 绝对路径
	$k = fopen($filename, "a");
	@fwrite($k, $str);
	fclose($k);
}

function read($filename) { #$filename 绝对路径
	$handle = fopen($filename, "r");
	$contents = fread($handle, filesize($filename));
	fclose($handle);
	if (false === $contents)
		return NULL;
	else
		return $contents;
}
