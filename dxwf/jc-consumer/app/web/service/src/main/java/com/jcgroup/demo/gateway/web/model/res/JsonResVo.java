package com.jcgroup.demo.gateway.web.model.res;


import com.jcgroup.demo.gateway.service.exception.ErrorEnum;

/**
 * @author jim
 * @date 16/10/12
 */
public class JsonResVo {
    //信息码，0表示成功，其他表示对比错误
    private int code;
    //错误消息
    private String errmsg;
    //返回数据对象
    private Object data;


    // ========= build succeed ========= //
    public static JsonResVo buildSuccess() {
        return buildSuccess(null);
    }

    public static JsonResVo buildSuccess(Object data) {
        return build(ResultStatusCode.OK.getErrcode(), null, data);
    }


    // ========= build failed  ========= //
    public static JsonResVo buildFail(ErrorEnum errorEnum) {
        return buildErrorResult(errorEnum.getErrorCode(), errorEnum.getErrorMessage());
    }

    public static JsonResVo buildErrorResult(int code, String errmsg) {
        return buildErrorResult(code, errmsg, null);
    }

    public static JsonResVo buildErrorResult(int code, String errmsg, Object data) {
        return build(code, errmsg, data);
    }


    private static JsonResVo build(int code, String errmsg, Object data) {
        JsonResVo jsonResVo = new JsonResVo();
        jsonResVo.setCode(code);
        jsonResVo.setErrmsg(errmsg);
        jsonResVo.setData(data);
        return jsonResVo;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getErrmsg() {
        return errmsg;
    }

    public void setErrmsg(String errmsg) {
        this.errmsg = errmsg;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }
}
