<script lang="ts">
  import Button, { Label } from '@smui/button';
  import List, {
    Item,
    Meta,
    Text,
    PrimaryText,
    SecondaryText,
  } from '@smui/list';
  import {deleteDocument, getDocumentList, uploadDocument} from "../../services/documentsService";
  import {onMount} from "svelte";
  import {delay} from "../../utils/delay";
  import type {DocumentFile} from "../../types/document";
  import {formatDate} from "../../utils/date";
  import Dialog, { Title, Content, Actions } from '@smui/dialog';


  const ButtonName = '上传知识库';
  let buttonName = ButtonName;
  let deleteVisible = $state(false);
  let forDeletedDocument:DocumentFile = $state({
    file_name: '',
    file_size: 0,
    upload_time: Date(),
  });

  // 文件输入处理
  const handleFileInputChange = async (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      try {
        buttonName = '上传中...'
        await uploadDocument(target.files[0]);

        getDocuments();

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



  const deleteConfirmDialog = (document: DocumentFile) => {
    deleteVisible = true;
    forDeletedDocument = document;
  }

  const deleteConfirm = async () => {
    const res = await deleteDocument(forDeletedDocument.file_name)

    if (res.status === "success") {
      getDocuments();
    }
  }

  async function getDocuments() {
    documentList = await getDocumentList();
  }

  // 模拟文件数据（用于演示）
  let documentList: DocumentFile[] = $state([]);

  onMount(() => {
    getDocuments();
  })
</script>

<div class="document-tab">
  <!-- 文件列表区域 -->
  <div class="file-list-container">
    <List class="file-list">
      {#each documentList as document, i}
        <Item nonInteractive>
          <Text>
            <PrimaryText>{document.file_name}</PrimaryText>
            <SecondaryText>{formatDate(new Date(document.upload_time), 'YYYY-MM-DD HH:mm')}</SecondaryText>
          </Text>
          <Meta class="material-icons" onclick={() => deleteConfirmDialog(document)}>删除</Meta>
        </Item>
      {/each}
    </List>
  </div>

  <!-- 上传文件区域 -->
  <div class="upload-area" style:border-radius="8px">
    <div class="file-upload">
      <input 
        type="file" 
        id="file-input"
        class="file-input" 
        on:change={handleFileInputChange}
        accept=".pdf,.txt,.csv"
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

  <Dialog
          bind:open={deleteVisible}
          aria-labelledby="simple-title"
          aria-describedby="simple-content"
  >
    <Title id="simple-title">再次确定</Title>
    <Content id="simple-content">确定要删除{forDeletedDocument?.file_name}吗？</Content>
    <Actions>
      <Button variant="outlined" color="secondary" onclick={() => ('No')}>
        <Label>取消</Label>
      </Button>
      <Button variant="raised" onclick={deleteConfirm}>
        <Label>确定</Label>
      </Button>
    </Actions>
  </Dialog>
</div>

<style lang="scss">
  .document-tab {
    height: 100%;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .file-list-container {
    :global(.mdc-deprecated-list-item__secondary-text){
      font-size: 12px;
    }
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

  .document-tab{
    :global(.material-icons){
      color: #ff3e00;
      cursor: pointer;
      font-size: 12px;
    }
  }
</style>