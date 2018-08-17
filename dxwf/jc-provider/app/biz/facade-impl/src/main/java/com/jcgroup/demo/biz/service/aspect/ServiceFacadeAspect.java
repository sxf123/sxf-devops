package com.jcgroup.demo.biz.service.aspect;


import com.jcgroup.demo.core.service.exception.BizException;
import com.jcgroup.demo.core.service.exception.ErrorEnum;
import com.jcgroup.demo.core.service.exception.ServiceException;
import com.jcgroup.jcy.component.common.model.Result;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;
import java.util.Date;

/**
 * 服务请求拦截
 * 1.请求处理
 * 2.map转请求对象
 * @author jim
 * @date 16/10/12
 */
@Aspect
@Component
public class ServiceFacadeAspect {
    private static final Logger digestLogger = LoggerFactory.getLogger("SERVICE-DIGEST");
    private static final Logger defaultLogger = LoggerFactory.getLogger("SERVICE-DEFAULT");

    @Pointcut("execution(* com.jcgroup.demo.facade.*.*(..))")
    private void allMethod() {
    }

    @Around("allMethod()")
    public Object doAround(ProceedingJoinPoint call) throws Throwable {
        //TODO LOG 需要打印请求日志
        MethodSignature signature = (MethodSignature) call.getSignature();
        Method method = signature.getMethod();
        Result baseRes = (Result) method.getReturnType().newInstance();
        String[] classNameArray = method.getDeclaringClass().getName().split("\\.");
        String methodName = classNameArray[classNameArray.length - 1] + "." + method.getName();
        String params = buildParamsDefault(call);

        Date startDate = new Date();
        try {
            defaultLogger.info("[SERVICE_REQUEST]" + methodName + "," + params);
            baseRes = (Result) call.proceed();
            defaultLogger.info("[SERVICE_RESPONSE]" + ToStringBuilder.reflectionToString(baseRes, ToStringStyle.SHORT_PREFIX_STYLE));
            return baseRes;
        } catch (ServiceException e) {
            baseRes.setSuccess(false);
            baseRes.setCode(e.getErrorCode());
            baseRes.setMessage(e.getErrorMessage());
            defaultLogger.error("服务处理异常", e);
            return baseRes;
        } catch (BizException e) {
            baseRes.setSuccess(false);
            baseRes.setCode(e.getError().getErrorCode());
            baseRes.setMessage(e.getError().getErrorMessage());
            defaultLogger.error("业务处理异常", e);
            return baseRes;
        } catch (Exception e) {
            baseRes.setSuccess(false);
            baseRes.setCode(ErrorEnum.ERROR_DEFAULT.getErrorCode());
            baseRes.setMessage(ErrorEnum.ERROR_DEFAULT.getErrorMessage());
            defaultLogger.error("未知异常: " + e.getMessage(), e);
            return baseRes;
        } finally {
            defaultLogger.info("[SERVICE_RESPONSE]" + methodName + "," + baseRes);
            long runTimes = System.currentTimeMillis() - startDate.getTime();
            digestLogger.info(methodName + "," + baseRes.getCode() + "," + runTimes + "ms");
        }
    }

    private String buildParamsDefault(ProceedingJoinPoint call) {
        String params = "[";
        for (int i = 0; i < call.getArgs().length; i++) {
            Object obj = call.getArgs()[i];
            if (i != call.getArgs().length - 1) {
                params += obj + ",";
            } else {
                params += obj + "]";
            }
        }
        return params;
    }
}