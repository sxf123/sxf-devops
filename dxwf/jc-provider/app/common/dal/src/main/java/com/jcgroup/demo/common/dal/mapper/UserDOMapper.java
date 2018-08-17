package com.jcgroup.demo.common.dal.mapper;

import com.jcgroup.demo.common.dal.dataobject.UserDO;
import java.util.List;
import org.apache.ibatis.annotations.Param;

/**
 * 由于需要对分页支持,请直接使用对应的DAO类
 * 注意:此结构有系统生成,禁止手工修改,以免被覆盖,请通过dalgen生成
 * The Table USER.
 * USER
 */
public interface UserDOMapper{

    /**
     * desc:插入表:USER.<br/>
     * descSql =  SELECT LAST_INSERT_ID() INSERT INTO USER( USERNAME ,CREATE_TIME ,UPDATE_TIME )VALUES( #{username,jdbcType=VARCHAR} ,now() ,now() )
     * @param entity entity
     * @return Long
     */
    Long insert(UserDO entity);
    /**
     * desc:更新表:USER.<br/>
     * descSql =  UPDATE USER SET USERNAME = #{username,jdbcType=VARCHAR} ,UPDATE_TIME = now() WHERE ID = #{id,jdbcType=BIGINT}
     * @param entity entity
     * @return Long
     */
    Long update(UserDO entity);
    /**
     * desc:根据主键删除数据:USER.<br/>
     * descSql =  DELETE FROM USER WHERE ID = #{id,jdbcType=BIGINT}
     * @param id id
     * @return Long
     */
    Long deleteByPrimary(Long id);
    /**
     * desc:根据主键获取数据:USER.<br/>
     * descSql =  SELECT * FROM USER WHERE ID = #{id,jdbcType=BIGINT}
     * @param id id
     * @return UserDO
     */
    UserDO getByPrimary(Long id);
    /**
     * desc:取数据:USER.<br/>
     * descSql =  SELECT * FROM USER
     * @return List<UserDO>
     */
    List<UserDO> listUsers();
}
