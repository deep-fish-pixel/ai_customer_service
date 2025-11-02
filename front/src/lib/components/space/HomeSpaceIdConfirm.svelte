<script lang="ts">
    import Button, { Label } from '@smui/button';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import { navigate, useRouter, useLocation, useHistory } from "svelte5-router";
    import Dialog, { Title, Content, Actions } from '@smui/dialog';


    let focused = $state(false);
    let value: string | null = $state(null);
    let dirty = $state(false);
    let invalid = $state(false);
    const router = useRouter();
    const location = useLocation();
    const history = useHistory();

    let isSpace = $derived(history.location.pathname.match(/^\/space\/\w+$/));
    let visible = $state(!isSpace);

    // 正则表达式：只允许下划线、数字和字母
    const spaceIdRegex = /^\w+$/;

    // $effect(() => {
    //     if (!history.location.pathname.match(/^\/space\/\w+$/)) {
    //         visible = true;
    //     }
    // });

    function handlerChange() {
        if (value && value.trim()) {
            // 验证输入是否符合要求
            invalid = !spaceIdRegex.test(value);
        } else {
            invalid = true;
        }
        console.log('handlerChange======', value, invalid)
    }

    const confirm = async () => {
        navigate(`/space/${value}`);
    }
</script>

<Dialog
        bind:open={visible}
        aria-labelledby="simple-title"
        aria-describedby="simple-content"
        onclick={(e) => {
          // 禁止关闭
          setTimeout(() => {
            visible = true;
          }, 80)
        }}
>
    <Title id="simple-title">请输入个人空间</Title>
    <Content id="simple-content">
        <Textfield
            type="text"
            bind:dirty
            bind:invalid
            bind:value
            label="空间id"
            style="min-width: 450px;"
            oninput={handlerChange}
            inputAttributes={{ maxlength: 40 }}
          >
            {#snippet helper()}
                <HelperText validationMsg={invalid && dirty}>
                    {invalid && dirty ? '空间ID只能包含字母、数字和下划线' : ''}
                </HelperText>
            {/snippet}
        </Textfield>
    </Content>
    <Actions>
        <Button variant="raised" disabled={!value || invalid} onclick={confirm}>
            <Label>确定</Label>
        </Button>
    </Actions>
</Dialog>

<style lang="scss">
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