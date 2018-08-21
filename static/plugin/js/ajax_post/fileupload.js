$("#input-b2").fileinput({
    uploadUrl: "http://127.0.0.1:8000/deploy/upload/",
    allowFileExtensions: ['sql'],
    overwriteInitial: false,
    maxFileSize: 1500,
    maxFileNum: 10,
    slugCallback: function(filename){
        return filename;
    }
});