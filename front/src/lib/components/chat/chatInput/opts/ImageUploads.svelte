<script lang="ts">
  import Button, { Label } from '@smui/button';
  import {deleteDocument, getDocumentList, uploadDocument} from "../../../../services/documentsService";
  import {onMount} from "svelte";
  import {delay} from "../../../../utils/delay";
  import type {DocumentFile} from "../../../../types/document";
  import Dialog, { Title, Content, Actions } from '@smui/dialog';
  import {showToast} from "../../../../utils/toast";
  import {getUserId} from "../../../../state/userState.svelte";
  import PlusIcon from "../../../../icons/PlusIcon.svelte";


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
      // 限制文件1M内
      if (target.files[0].size > 1024 * 1024) {
        showToast("文件大小不能超过1M");
        return;
      }
      try {
        await uploadDocument(target.files[0]);

        showToast("上传文件成功");
        getDocuments();

      } catch (err: any) {
        showToast("上传文件失败：" + err.message);
      }

      // 重置input以便可以再次上传相同的文件
      target.value = '';
    }
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
    if(getUserId()) {
      documentList = await getDocumentList();
    }
  }

  // 模拟文件数据（用于演示）
  let documentList: DocumentFile[] = $state([]);

  onMount(() => {
    getDocuments();
  })
</script>

<div class="image-uploader">
  <!-- 上传文件区域 -->
  <div class="upload-area">
    <img width="62px" height="72px" src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"/>
    <div class="remove">-</div>
  </div>
  <div class="upload-area">
    <img width="62px" height="72px" src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"/>
    <div class="remove">-</div>
  </div>
  <div class="upload-area">
    <div class="file-upload">
      <input 
        type="file" 
        id="file-input"
        class="file-input" 
        on:change={handleFileInputChange}
        accept=".pdf,.txt,.csv,.md,.docx,.xlsx"
      />
      <Button
        class="file-button"
        variant="raised"
        color="primary"
        disabled={!getUserId()}
      >
        <div class="upload-text">
          <PlusIcon />
          <p>添加</p>
        </div>
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
  .image-uploader {
    height: 72px;
    padding: 6px 0;
    display: flex;
    flex-direction: row;

    .upload-area {
      width: 62px;
      height: 72px;
      margin-left: 8px;
      position: relative;

      &:hover{
        .remove{
          display: block;
        }
      }

      img{
        border-radius: 4px;
      }
      .remove{
        width: 14px;
        height: 14px;
        font-size: 16px;
        color: #fff;
        background: #000;
        border-radius: 14px;
        position: absolute;
        top: -5px;
        right: -5px;
        z-index: 1;
        line-height: 11px;
        text-align: center;
        cursor: pointer;
        display: none;
      }
    }

    .file-upload{
      position: relative;
      height: 100%;

      .file-input {
        opacity: 0;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        cursor: pointer;
      }

      :global(.file-button){
        width: 100%;
        height: 100%;
        background-color: #fff;
        box-shadow: none;
        border: 1px solid #eee;
        border-radius: 4px;
      }
    }

    .upload-text{
      color: rgb(102, 102, 102);
      p{
        font-size: 12px;
        padding: 0;
        margin: 0;
      }
    }
  }

  .section-title {
    margin-bottom: 16px;
    color: rgba(0, 0, 0, 0.87);
  }

  .empty-state {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(0, 0, 0, 0.6);
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
    :global(.mdc-deprecated-list-item__secondary-text){
      font-size: 12px;
    }
    :global(.file-list) {
      flex: 1;
      overflow-y: auto;
      padding: 0;
    }
    :global(.file-item){
      padding: 0;
      margin-bottom: 10px;
    }
    :global(.material-icons){
      width: 60px;
      text-align: right;
      font-size: 14px;
      color: var(--mdc-text-button-label-text-color, var(--mdc-theme-primary, #6200ee));
      cursor: pointer;
    }
  }
</style>