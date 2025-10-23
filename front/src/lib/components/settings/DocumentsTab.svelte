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
  import {getDocumentList, uploadDocument} from "../../services/documentsService";
  import {onMount} from "svelte";
  import {delay} from "../../utils/delay";
  import type {DocumentFile} from "../../types/document";
  import {formatDate} from "../../utils/date";

  const ButtonName = '上传知识库';
  let buttonName = ButtonName;

  // 文件输入处理
  const handleFileInputChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      try {
        buttonName = '上传中...'
        uploadDocument(target.files[0]);

        delay(300, () => {
          buttonName = ButtonName;
        });

      } catch (err) {
        delay(300, () => {
          buttonName = ButtonName;
        });
      }

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
  let documentList: DocumentFile[] = [];

  onMount(async () => {
    const list = await getDocumentList();

    documentList = list;
  })
</script>

<div class="knowledge-base-tab">
  <!-- 文件列表区域 -->
  <Paper elevation={1} class="file-list-container">
    <List class="file-list">
      {#each documentList as document, i}
        <Item nonInteractive>
          <Text>
            <PrimaryText>{document.file_name}</PrimaryText>
            <SecondaryText>{formatDate(new Date(document.upload_time), 'YYYY-MM-DD HH:mm')}</SecondaryText>
          </Text>
          <Meta class="material-icons">删除</Meta>
        </Item>
      {/each}
    </List>
  </Paper>

  <!-- 上传文件区域 -->
  <div class="upload-area" style:border-radius="8px">
    <div class="file-upload">
      <input 
        type="file" 
        id="file-input"
        class="file-input" 
        on:change={handleFileInputChange}
        accept=".pdf,.txt,.xls,.md"
      />
      <Button
        class="file-button"
        variant="raised"
        color="primary"
      >
        { buttonName }
      </Button>
    </div>
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

  .file-upload{
    position: relative;

    .file-input {
      opacity: 0;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }

    :global(.file-button){
      width: 100%;
    }

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