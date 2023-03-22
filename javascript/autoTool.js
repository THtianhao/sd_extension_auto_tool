//function clear_loaded() {
//    for (let arg in arguments){
//
//    }
//    return "";
//}

function filterArgs(argsCount, arguments) {
    let args_out = [];
    if (arguments.length >= argsCount && argsCount !== 0) {
        for (let i = 0; i < argsCount; i++) {
            args_out.push(arguments[i]);
        }
    }
    return args_out;
}