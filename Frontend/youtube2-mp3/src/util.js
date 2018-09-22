var getVideoId = (url) => {
    let tmp_value = url.split("v=");

    if(tmp_value.length === 2)
    {
        let id_value = tmp_value[1].substr(0,11);

        if(id_value.length === 11)
            return id_value;
        else
            return "";
    }

    return "";
}

exports.getVideoId = getVideoId;