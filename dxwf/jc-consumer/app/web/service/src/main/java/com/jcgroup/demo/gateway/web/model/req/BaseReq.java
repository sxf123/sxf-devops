package com.jcgroup.demo.gateway.web.model.req;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.jcgroup.demo.gateway.web.utils.ParamsUtil;

import java.util.HashMap;
import java.util.Map;

/**
 * @author jim
 * @date 16/10/12
 */
public class BaseReq {

    private String accessToken;

    private String clientVersion;

    // A, I
    @JsonProperty(value = "OSType")
    private String OSType;

    public String getAccessToken() {
        return accessToken;
    }

    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }

    public String getClientVersion() {
        return clientVersion;
    }

    public void setClientVersion(String clientVersion) {
        this.clientVersion = clientVersion;
    }

    public String getOSType() {
        return OSType;
    }

    public void setOSType(String OSType) {
        this.OSType = OSType;
    }

    /**
     * 检查参数是否合法
     *
     * @return
     */
    public void checkData() {
        Map<String, Object> checkParam = new HashMap<>();
        ParamsUtil.hasEmptyParamMap(checkParam);
    }
}
