package com.jcgroup.demo.core.service.exception;

/**
 * 业务错误
 *
 * @author jim
 * @date 16/10/12
 */
public class BizException extends RuntimeException {
    private ErrorEnum error = null;
    private String message;

    public BizException() {
        this.error = ErrorEnum.ERROR_DEFAULT;
        this.message = ErrorEnum.ERROR_DEFAULT.getErrorMessage();
    }

    public BizException(String message) {
        this.error = ErrorEnum.ERROR_DEFAULT;
        this.message = message;
    }

    public BizException(ErrorEnum error) {
        this.error = error;
        this.message = error.getErrorMessage();
    }

    public BizException(ErrorEnum error, String message) {
        this.error = error;
        this.message = message;
    }

    public ErrorEnum getError() {
        return error;
    }

    public void setError(ErrorEnum error) {
        this.error = error;
    }

    @Override
    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
