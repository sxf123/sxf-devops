package com.jcgroup.demo.gateway.web.controller;

import com.jcgroup.demo.gateway.web.model.req.BaseReq;
import com.jcgroup.demo.gateway.web.model.res.JsonResVo;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 *
 * @author jim
 * @date 2018/1/12
 */
@RestController
@RequestMapping(value = "/index", method = RequestMethod.POST, consumes = "application/json;charset=UTF-8")
public class TestController {

    @RequestMapping(path = "/test")
    public JsonResVo cardCount(@RequestBody BaseReq req) {

        return JsonResVo.buildSuccess("Hello JWS 1.0");
    }

}
