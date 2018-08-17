package com.jcgroup.demo.gateway.service.exception;

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
    //1开头返回接收细节错误码,其它返回父错误码
    SYSTEM_ERROR(10000, 10000, "系统错误"),//
    ERROR_BIZ_FAIL(10000, 10001, "业务失败"),
    ERROR_BIZ_UNIQUE_REQ_ID(10000, 10002, "唯一性约束重复"),
    SERVICE_ERROR(10000, 90001, "服务错误"),

    //2开头为参数校验信息错误
    ERROR_PARAM(20000, 20000, "参数错误"),
    ERROR_PARAM_EMPTY(20000, 20001, "参数为空"),
    ERROR_PARAM_FORMAT(20000, 20002, "参数格式不正确"),
    ERROR_PARAM_KEY_NOT_EXIST(20000, 20007, "参数不存在"),
    ERROR_PARAM_TEMPLATE_TYPE_INVALID(20000,20008,"模板类型无效"),
    ERROR_SMS_SEND_FAIL(20000,20009,"短信发送失败"),
    ERROR_TOKEN_EXPIRE(20000, 20101, "登陆失效"),


    ERROR_GET_RECHARGE_CONFIG(30000,30001,"获取充值列表失败！"),
    ERROR_PAY_SIGN(30000,30002,"支付签名失败"),

    ERROR_PAY_USER(30000,30003,"只能自己或者代付人付款！"),
    ERROR_PAY_ORDER_STATUS(30000,30004,"订单已取消！"),
    ERROR_PAY_ORDER_PAY_STATUS(30000,30005,"订单当前状态不可以发起支付！"),

    ERROR_PAY_METHOD(30000,30006,"支付方式错误"),


    ERROR_PERMISSION_DENIED(50000,50110,"抱歉，您暂无权限查看"),
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
