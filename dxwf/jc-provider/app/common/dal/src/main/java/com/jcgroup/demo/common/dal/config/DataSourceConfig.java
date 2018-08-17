package com.jcgroup.demo.common.dal.config;

import com.alibaba.druid.pool.DruidDataSource;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInterceptor;
import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.SqlSessionTemplate;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;
import java.util.Properties;

/**
 * @author jim
 * @date 16/10/12
 */
@Configuration
@EnableTransactionManagement(proxyTargetClass = true)
@MapperScan(basePackages = {"com.jcgroup.demo.common.dal"}, sqlSessionFactoryRef = "sqlSessionFactory")
public class DataSourceConfig {

    @Value("${datasource.general-mysql.url}")
    private String url;

    @Value("${datasource.general-mysql.username}")
    private String userName;

    @Value("${datasource.general-mysql.password}")
    private String password;

    @Value("${datasource.general-mysql.driver-class-name}")
    private String driverClassName;

    @Value("${datasource.general-mysql.max-idle}")
    private String maxIdle;

    @Value("${datasource.general-mysql.min-idle}")
    private String minIdle;

    @Value("${datasource.general-mysql.max-wait}")
    private String maxWait;

    @Value("${datasource.general-mysql.initial-size}")
    private String initialSize;

    @Value("${datasource.general-mysql.max-active}")
    private String maxActive;

    @Value("${datasource.minEvictableIdleTimeMillis}")
    private String minEvictableIdleTimeMillis;


    @Primary
    @Bean
    public DataSource dataSource() {
        DruidDataSource datasource = new DruidDataSource();
        datasource.setUrl(url);
        datasource.setDriverClassName(driverClassName);
        datasource.setUsername(userName);
        datasource.setPassword(password);
        datasource.setInitialSize(Integer.valueOf(initialSize));
        datasource.setMinIdle(Integer.valueOf(minIdle));
        datasource.setMaxWait(Long.valueOf(maxWait));
        datasource.setMaxActive(Integer.valueOf(maxActive));
        datasource.setMinEvictableIdleTimeMillis(Long.valueOf(minEvictableIdleTimeMillis));
        return datasource;
    }

    @Primary
    @Bean(name = "transactionManager")
    public DataSourceTransactionManager transactionManager(@Qualifier("dataSource") DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }

    @Primary
    @Bean(name = "sqlSessionFactory")
    public SqlSessionFactory sqlSessionFactory(@Qualifier("dataSource") DataSource dataSource) throws Exception {
        SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
        factoryBean.setDataSource(dataSource);
        String path = "classpath*:com.jcgroup.jcy.activity.common.dal.mapper/*.xml";
        factoryBean.setMapperLocations(new PathMatchingResourcePatternResolver().getResources(path));

        //添加分页插件
        addPageHelperPlugin(factoryBean);


        return factoryBean.getObject();
    }

//    @Bean
//    public PageHelper pageHelper(){
//        PageHelper pageHelper = new PageHelper();
//        Properties properties = new Properties();
//        properties.setProperty("offsetAsPageNum", "true");
//        properties.setProperty("rowBoundsWithCount", "true");
//        properties.setProperty("reasonable", "true");
//        properties.setProperty("helperDialect", "mysql");
//        pageHelper.setProperties(properties);
//        return pageHelper;
//    }

    private void addPageHelperPlugin(SqlSessionFactoryBean sessionFactoryBean) throws Exception {
        PageInterceptor interceptor = new PageInterceptor();
        Properties properties = new Properties();
        properties.setProperty("helperDialect", "mysql");
        properties.setProperty("reasonable", "true");
        interceptor.setProperties(properties);
        sessionFactoryBean.getObject().getConfiguration().addInterceptor(interceptor);
    }

    @Bean(name = "sqlSessionTemplate")
    @Primary
    public SqlSessionTemplate sqlSessionTemplate(@Qualifier("sqlSessionFactory") SqlSessionFactory sqlSessionFactory) throws Exception {
        return new SqlSessionTemplate(sqlSessionFactory);
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getDriverClassName() {
        return driverClassName;
    }

    public void setDriverClassName(String driverClassName) {
        this.driverClassName = driverClassName;
    }
}
