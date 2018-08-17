package com.jcgroup.demo.facade.service.vo;

import java.io.Serializable;
import java.util.Date;

/**
 * @author jim
 * @date 16/10/12
 */
public class UserVO implements Serializable {


    private static final long serialVersionUID = -7391389973328711766L;

    /**
     * id ID.
     */
    private Long id;
    /**
     * username USERNAME.
     */
    private String username;
    /**
     * createTime CREATE_TIME.
     */
    private Date createTime;
    /**
     * updateTime UPDATE_TIME.
     */
    private Date updateTime;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Date getUpdateTime() {
        return updateTime;
    }

    public void setUpdateTime(Date updateTime) {
        this.updateTime = updateTime;
    }
}
