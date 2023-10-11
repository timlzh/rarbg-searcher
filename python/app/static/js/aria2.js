class Aria2 {
    constructor(endPoint, token) {
        console.log('Aria2 constructor');
        console.log(endPoint);
        this.endPoint = endPoint;
        this.token = token;
    }

    addUris(uri) {
        console.log('Aria2 addUri');
        console.log(uri);
        $.jsonRPC.setup({
            endPoint: this.endPoint,
            namespace: 'aria2'
        });

        let methods = []
        for (let i = 0; i < uri.length; i++) {
            methods.push({
                method: 'addUri',
                params: [
                    'token:' + this.token,
                    [uri[i]]
                ]
            })
        }
        $.jsonRPC.batchRequest(methods, {
            success: function (response) {
                console.log(response);
                alert("已发送" + uri.length + "个任务");
                window.history.back();
            },
            error: function (response) {
                console.log(response);
                alert("发送失败");
                window.history.back();
            }
        });
    }
}