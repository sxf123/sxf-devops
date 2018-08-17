package com.jcgroup.demo.core.service.manager;

import com.jcgroup.demo.common.dal.dao.UserDAO;
import com.jcgroup.demo.common.dal.dataobject.UserDO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author jim
 * @date 16/10/12
 */
@Service
public class DemoServiceImpl implements DemoService {

    @Autowired
    UserDAO userDAO;


    @Override
    public List<UserDO> listUsers() {
        return userDAO.listUsers();
    }

    @Override
    public UserDO getUser(Long id) {
        return userDAO.getByPrimary(id);
    }

    @Override
    public void addUser(UserDO userDO) {
         userDAO.insert(userDO);
    }

    @Override
    public void updateUser(UserDO userDO) {
        userDAO.update(userDO);

    }
}
