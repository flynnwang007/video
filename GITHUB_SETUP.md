# GitHub设置指南

按照以下步骤将此项目推送到您的GitHub账号：

## 1. 创建GitHub仓库

1. 登录您的GitHub账号
2. 点击右上角的"+"图标，选择"New repository"
3. 填写仓库名称，例如"video_tool"
4. 添加描述（可选）："一个简单易用的视频平台API工具"
5. 保持仓库为公开或选择私有
6. 不要初始化仓库（不勾选"Initialize this repository with a README"）
7. 点击"Create repository"

## 2. 关联并推送本地仓库

执行以下命令，将您的本地仓库关联到GitHub并推送代码：

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/video_tool.git

# 推送代码到远程仓库
git push -u origin master
```

## 3. 验证

1. 刷新GitHub仓库页面
2. 确认所有文件已成功上传
3. 点击"Settings"标签，确认仓库设置

## 4. 进一步设置（可选）

- 在GitHub上添加项目标签和主题
- 设置项目网站
- 添加持续集成（如GitHub Actions）
- 添加协作者（如果是团队项目）

## 5. 克隆仓库到其他设备

在其他计算机上使用以下命令克隆仓库：

```bash
git clone https://github.com/你的用户名/video_tool.git
cd video_tool
```

## 注意事项

- 确保`.gitignore`文件已正确配置，以避免上传敏感信息
- 敏感信息（如API密钥）应存储在`.env`文件中，且该文件不应被提交
- 定期提交和推送更改，以保持代码同步 