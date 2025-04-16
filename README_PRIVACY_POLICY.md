# 隐私政策页面部署指南

本文档提供了将隐私政策页面部署到您的API服务器的步骤。

## 文件说明

- `privacy_policy.html` - 隐私政策页面HTML文件
- `deploy_privacy_policy.sh` - 自动部署脚本

## 部署步骤

### 1. 将文件上传到服务器

使用scp将文件上传到您的服务器:

```bash
scp privacy_policy.html deploy_privacy_policy.sh root@your_server_ip:~/
```

请将 `your_server_ip` 替换为您的服务器IP地址（例如 14.103.200.105）。

### 2. 登录到服务器

```bash
ssh root@your_server_ip
```

### 3. 执行部署脚本

```bash
cd ~/
chmod +x deploy_privacy_policy.sh
./deploy_privacy_policy.sh
```

### 4. 验证部署

脚本执行完成后，在浏览器中访问以下地址验证隐私政策页面是否正确显示:

```
https://api.aibase123.com
```

## 注意事项

- 这个配置保留了API的所有功能，您仍然可以通过 `/api/` 路径访问原有的API
- 脚本保留了Let's Encrypt证书自动续期所需的验证路径
- 如果您修改了隐私政策内容，只需重新运行部署脚本即可更新

## 自定义

如果您需要修改隐私政策内容:

1. 编辑 `privacy_policy.html` 文件
2. 重新运行部署脚本

## 故障排除

如果部署后出现问题:

1. 检查Nginx错误日志:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

2. 确认Nginx配置是否正确:
   ```bash
   sudo nginx -t
   ```

3. 检查文件权限:
   ```bash
   ls -la /var/www/html/
   ```

如果您需要进一步帮助，请联系: fly555888@126.com 