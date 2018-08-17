package com.jcgroup.demo.core.service.manager;

import com.jcgroup.demo.common.dal.dataobject.UserDO;

import java.util.List;

/**
 * @author jim
 * @date 16/10/12
 */
public interface DemoService {

    List<UserDO> listUsers();

    UserDO getUser(Long id);

    void addUser(UserDO userDO);

    void updateUser(UserDO userDO);
}
