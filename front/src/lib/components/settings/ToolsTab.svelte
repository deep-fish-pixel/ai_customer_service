<script lang="ts">
  import Card, { Content } from '@smui/card';
  import Switch from '@smui/switch';
  import Paper, { Title } from '@smui/paper';
  import type {ToolConfig} from "../../types";
  


  // 从父组件接收的属性
  export let tools: ToolConfig[] = [];
  export let onToolToggle: (toolId: string, enabled: boolean) => void;

  // 模拟工具数据
  const demoTools: ToolConfig[] = [
    {
      id: 'qa',
      name: '基础问答',
      description: '提供简单问题的快速回答',
      enabled: true
    },
    {
      id: 'knowledge',
      name: '知识库检索',
      description: '从上传的文件中检索信息',
      enabled: true
    },
    {
      id: 'context',
      name: '上下文理解',
      description: '理解对话上下文进行连续对话',
      enabled: true
    }
  ];

  // 如果没有传入工具数据，使用演示数据
  $: displayTools = tools.length > 0 ? tools : demoTools;
</script>

<div class="tools-tab">
  <Paper elevation={1} class="tools-container">
    <Title variant="h6" class="section-title">工具功能</Title>
    
    <div class="tools-list">
      {#each displayTools as tool}
        <Card class="tool-item">
          <Content>
            <div class="tool-header">
              <div class="tool-info">
                <Title variant="subtitle1" class="tool-name">{tool.name}</Title>
                <Title variant="body2" color="textSecondary">{tool.description}</Title>
              </div>
              <Switch
                checked={tool.enabled}
                color="primary"
              />
            </div>
          </Content>
        </Card>
      {/each}
    </div>

    <Paper elevation={0} class="coming-soon">
      <Title variant="body2" color="textSecondary">
        更多工具功能即将推出
      </Title>
    </Paper>
  </Paper>
</div>

<style lang="scss">
  .tools-tab {
    height: 100%;
    padding: 16px;
  }

  .tools-container {
    height: 100%;
    padding: 16px;
    display: flex;
    flex-direction: column;
  }

  .section-title {
    margin-bottom: 16px;
    color: rgba(0, 0, 0, 0.87);
  }

  .tools-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
    overflow-y: auto;
    padding-bottom: 16px;
  }

  .tool-item {
    border-radius: 8px;
    overflow: hidden;
  }

  .tool-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .tool-info {
    flex: 1;
    margin-right: 16px;
  }

  .tool-name {
    font-weight: 500;
    margin-bottom: 4px;
  }

  .coming-soon {
    margin-top: auto;
    padding: 12px;
    text-align: center;
    background-color: #f5f5f5;
    border-radius: 8px;
  }
</style>