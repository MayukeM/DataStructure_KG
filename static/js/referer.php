function getRemoteFile($url, $refer = '') {
    $option = array(
            'http' => array(
                'header' => "Referer:$refer")
            );
    $context = stream_context_create($option);
    return file_get_contents($url, false, $context);
}