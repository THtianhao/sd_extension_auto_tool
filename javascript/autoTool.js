function clear_loaded() {
    for (let arg in arguments){
    }
    alert("clear_loaded")
    return "";
}

function redirectToLark() {
    window.open('https://open.feishu.cn/open-apis/authen/v1/index?app_id=cli_a483ea8b94e3100e&redirect_uri=http://127.0.0.1', '_blank');
}

function redirectToRul(url){
    window.open(url, '_blank');
}

function filterArgs(argsCount, arguments) {
    let args_out = [];
    if (arguments.length >= argsCount && argsCount !== 0) {
        for (let i = 0; i < argsCount; i++) {
            args_out.push(arguments[i]);
        }
    }
    return args_out;
}