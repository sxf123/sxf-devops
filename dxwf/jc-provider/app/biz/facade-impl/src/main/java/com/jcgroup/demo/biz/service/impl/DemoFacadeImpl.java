package com.jcgroup.demo.biz.service.impl;

import com.alibaba.dubbo.config.annotation.Service;
import com.google.common.collect.Lists;
import com.jcgroup.demo.common.dal.dataobject.UserDO;
import com.jcgroup.demo.core.service.manager.DemoService;
import com.jcgroup.demo.facade.service.facade.DemoFacade;
import com.jcgroup.jcy.component.common.model.Result;
import com.jcgroup.demo.facade.service.vo.UserVO;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

/**
 * @author jim
 * @date 16/10/12
 */

@Service(version = "1.0.0")
public class DemoFacadeImpl implements DemoFacade {

    @Autowired
    DemoService demoService;

    @Override
    public Result<List<UserVO>> listUsers() {
        List<UserDO> userDOS = demoService.listUsers();
        if(userDOS!=null && !userDOS.isEmpty()){
            List<UserVO> userVOS = Lists.newArrayList();
            for(UserDO userDO : userDOS){
                UserVO userVO = new UserVO();
                BeanUtils.copyProperties(userDO, userVO);
                userVOS.add(userVO);
            }
            return Result.wrapSuccessfulResult(userVOS);
        }
        return Result.wrapSuccessfulResult(null);
    }

    @Override
    public Result<UserVO> getUser(Long id) {
        UserDO userDO = demoService.getUser(id);
        if(userDO !=null) {
            UserVO userVO = new UserVO();
            BeanUtils.copyProperties(userDO, userVO);
            return Result.wrapSuccessfulResult(userVO);
        }
        return Result.wrapSuccessfulResult(null);
    }

    @Override
    public Result<Boolean> addUser(UserVO userVO) {
        if(userVO != null){
            UserDO userDO = new UserDO();
            BeanUtils.copyProperties(userVO, userDO);
            demoService.addUser(userDO);
            return Result.wrapSuccessfulResult(true);
        }
        return Result.wrapSuccessfulResult(false);
    }

    @Override
    public Result<Boolean> updateUser(UserVO userVO) {
        if(userVO != null){
            UserDO userDO = new UserDO();
            BeanUtils.copyProperties(userVO, userDO);
            demoService.updateUser(userDO);
            return Result.wrapSuccessfulResult(true);
        }
        return Result.wrapSuccessfulResult(false);
    }
}
