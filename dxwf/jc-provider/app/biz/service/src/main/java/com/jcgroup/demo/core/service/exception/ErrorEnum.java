package com.jcgroup.demo.core.service.exception;
/**
 * 错误码
 * @author jim
 * @date 16/10/12
 */
public enum ErrorEnum {
    /**
     * 错误码分内外两种
     * 对内使用最细粒度错误吗，对外使用统一错误码
     * 对外统一使用本类型第一个错误码。
     */
    //1开头为对外不可以接收细节错误码
    ERROR_DEFAULT(10000, 10000, "系统异常"),

    //2开头为参数校验信息错误
    ERROR_PARAM(20000, 20000, "参数错误"),
    ERROR_PARAM_EMPTY(20000, 20001, "参数为空"),
    ERROR_PARAM_FORMAT(20000, 20002, "参数格式不正确"),
    ERROR_PARAM_KEY_NOT_EXIST(20000, 20007, "参数不存在"),
    ERROR_PARAM_TEMPLATE_TYPE_INVALID(20000,20008,"模板类型无效"),
    ERROR_SMS_SEND_FAIL(20000,20009,"短信发送失败"),
    ;

    private final int errorCode;
    private final int parentCode;
    private final String errorMessage;

    ErrorEnum(int parentCode, int errorCode, String errorMessage) {
        this.parentCode = parentCode;
        this.errorCode = errorCode;
        this.errorMessage = errorMessage;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public int getErrorCode() {
        return errorCode;
    }

    public int getParentCode() {
        if (String.valueOf(errorCode).startsWith("1")) {
            return errorCode;
        }

        return parentCode;
    }

    public ErrorEnum getOutError() {
        return getErrorByCode(getParentCode());
    }

    public static ErrorEnum getErrorByCode(int code) {
        for (ErrorEnum errorEnum : values()) {
            if (errorEnum.getErrorCode() == code) {
                return errorEnum;
            }
        }
        return null;
    }
}
