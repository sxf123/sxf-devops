package com.jcgroup.demo.facade.service.facade;

import com.jcgroup.jcy.component.common.model.Result;
import com.jcgroup.demo.facade.service.vo.UserVO;

import java.util.List;

/**
 * User: yingjing
 * Date: 2017/9/5 0005
 * Time: 下午 8:42
 */
public interface DemoFacade {

    Result<List<UserVO>> listUsers();

    Result<UserVO> getUser(Long id);

    Result<Boolean> addUser(UserVO userVO);

    Result<Boolean> updateUser(UserVO userVO);

}
