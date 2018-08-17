package com.jcgroup.demo.common.dal.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import com.jcgroup.demo.common.dal.dataobject.UserDO;
import java.util.List;
import com.jcgroup.demo.common.dal.mapper.UserDOMapper;

/**
* The Table USER.
* 注意:此结构有系统生成,禁止手工修改,以免被覆盖,请通过dalgen生成
* USER
*/
@Repository
public class UserDAO{

    @Autowired
    private UserDOMapper userDOMapper;

    /**
     * desc:插入表:USER.<br/>
     * descSql =  SELECT LAST_INSERT_ID() INSERT INTO USER( USERNAME ,CREATE_TIME ,UPDATE_TIME )VALUES( #{username,jdbcType=VARCHAR} ,now() ,now() )
     * @param entity entity
     * @return Long
     */
    public Long insert(UserDO entity){
        return userDOMapper.insert(entity);
    }
    /**
     * desc:更新表:USER.<br/>
     * descSql =  UPDATE USER SET USERNAME = #{username,jdbcType=VARCHAR} ,UPDATE_TIME = now() WHERE ID = #{id,jdbcType=BIGINT}
     * @param entity entity
     * @return Long
     */
    public Long update(UserDO entity){
        return userDOMapper.update(entity);
    }
    /**
     * desc:根据主键删除数据:USER.<br/>
     * descSql =  DELETE FROM USER WHERE ID = #{id,jdbcType=BIGINT}
     * @param id id
     * @return Long
     */
    public Long deleteByPrimary(Long id){
        return userDOMapper.deleteByPrimary(id);
    }
    /**
     * desc:根据主键获取数据:USER.<br/>
     * descSql =  SELECT * FROM USER WHERE ID = #{id,jdbcType=BIGINT}
     * @param id id
     * @return UserDO
     */
    public UserDO getByPrimary(Long id){
        return userDOMapper.getByPrimary(id);
    }
    /**
     * desc:取数据:USER.<br/>
     * descSql =  SELECT * FROM USER
     * @return List<UserDO>
     */
    public List<UserDO> listUsers(){
        return userDOMapper.listUsers();
    }
}
