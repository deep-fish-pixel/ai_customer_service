<script lang="ts">
  import Button from '@smui/button';
  // import { List, ListItem, ListItemText, ListItemSecondaryAction } from '@smui/list';
  import List, {
    Item,
    Graphic,
    Meta,
    Text,
    PrimaryText,
    SecondaryText,
  } from '@smui/list';
  import IconButton from '@smui/icon-button';
  import Paper, { Content } from '@smui/paper';
  import type {FileItem} from "../../types";
  
  // 从父组件接收的属性
  export let files: FileItem[] = [];
  export let onFileUpload: (file: File) => void;
  export let onFileDelete: (fileId: string) => void;
  export let onFileView: (fileId: string) => void;

  // 文件输入处理
  const handleFileInputChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      onFileUpload(target.files[0]);
      // 重置input以便可以再次上传相同的文件
      target.value = '';
    }
  };

  // 格式化文件大小
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // 模拟文件数据（用于演示）
  const demoFiles: FileItem[] = [
    {
      id: '1',
      name: '用户手册.pdf',
      uploadTime: '2024-10-22 10:30',
      size: 2048000
    },
    {
      id: '2', 
      name: '产品介绍.docx',
      uploadTime: '2024-10-21 14:45',
      size: 1536000
    }
  ];

  // 如果没有传入文件数据，使用演示数据
  $: displayFiles = files.length > 0 ? files : demoFiles;
</script>

<div class="knowledge-base-tab">
  <!-- 文件列表区域 -->
  <Paper elevation={1} class="file-list-container">
    <Content class="section-title">已上传的文件</Content>
    
    {#if displayFiles.length > 0}
      <List class="file-list">
        {#each displayFiles as file}
          <!--<ListItem>
            <ListItemText 
              primary={file.name}
              secondary={`${file.uploadTime} · ${formatFileSize(file.size)}`}
            />
            <ListItemSecondaryAction>
              <IconButton 
                onclick={() => onFileView?.(file.id)}
                aria-label="查看"
                size="mini"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                  <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                </svg>
              </IconButton>
              <IconButton
                      onclick={() => onFileDelete?.(file.id)}
                aria-label="删除"
                size="mini"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>-->
        {/each}
      </List>
    {:else}
      <div class="empty-state">
        <Content>暂无上传的文件</Content>
      </div>
    {/if}
  </Paper>

  <!-- 上传文件区域 -->
  <div class="upload-area" style:border-radius="8px">
    <input 
      type="file" 
      id="file-upload" 
      class="file-input" 
      on:change={handleFileInputChange}
      accept=".pdf,.doc,.docx,.txt,.xls,.xlsx,.ppt,.pptx"
    />
    <label for="file-upload">
      <Button 
        variant="outlined"
        color="primary"
      >
        上传文件
      </Button>
    </label>
  </div>
</div>

<style lang="scss">
  .knowledge-base-tab {
    height: 100%;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .file-list-container {
    flex: 1;
    padding: 16px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .section-title {
    margin-bottom: 16px;
    color: rgba(0, 0, 0, 0.87);
  }

  .file-list {
    flex: 1;
    overflow-y: auto;
  }

  .empty-state {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(0, 0, 0, 0.6);
  }

  .upload-area {
    padding: 16px 0;
  }

  .file-input {
    display: none;
  }

  :global(.MuiListItem-root) {
    border-radius: 8px;
    margin-bottom: 8px;
    transition: background-color 0.2s;

    &:hover {
      background-color: rgba(0, 0, 0, 0.04);
    }
  }
</style>