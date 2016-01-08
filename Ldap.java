package ad;

import java.util.Hashtable;

import javax.naming.Context;
import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;

public class Ldap {
	public static void main(String[] args) {
		String username = "username"; // 用户名
		String password = "password"; // 密码
		String host = "ladp-url"; // AD 服务器地址
		String port = "389"; // AD 端口
		String domain = "@mail.com"; // 域帐号邮箱后缀，必须有
		String url = new String("ldap://" + host + ":" + port);
		String user = username + domain;
		Hashtable<String, String> env = new Hashtable<String, String>();
		DirContext ctx;
		env.put(Context.SECURITY_AUTHENTICATION, "simple");// 以simple方式发送
		env.put(Context.SECURITY_PRINCIPAL, user); // 不带邮箱后缀名的话，会报错，具体原因还未探究
		env.put(Context.SECURITY_CREDENTIALS, password);
		env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
		env.put(Context.PROVIDER_URL, url);
		try {
			ctx = new InitialDirContext(env);
			ctx.close();
			System.out.println("验证成功！");
		} catch (NamingException err) {
			err.printStackTrace();
			System.out.println("验证失败！");
		}
	}
}
