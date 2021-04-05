<template>
  <v-card flat class="adapters">
    <v-row class="justify-center">
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="filterText"
          dense
          rounded
          outlined
          clearable
          hide-details
          label="搜索适配器"
        >
          <template v-slot:prepend-inner>
            <div class="v-input__icon v-input__icon--prepend-inner">
              <v-icon small>fa-filter</v-icon>
            </div>
          </template>
        </v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-dialog v-model="dialog" max-width="600px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn dark block color="primary" v-bind="attrs" v-on="on"
              >发布适配器
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">适配器信息</span>
            </v-card-title>
            <v-card-text>
              <v-form ref="newAdapterForm" v-model="valid" lazy-validation>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newAdapter.name"
                        label="协议名称"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newAdapter.desc"
                        label="协议介绍"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newAdapter.id"
                        label="PyPI 项目名"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newAdapter.link"
                        label="协议 import 包名"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newAdapter.repo"
                        label="仓库/主页链接"
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="dialog = false">
                关闭
              </v-btn>
              <v-btn
                :disabled="!valid"
                color="blue darken-1"
                text
                @click="
                  dialog = false
                  publishAdapter()
                "
              >
                发布
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
    <v-col cols="12">
      <v-pagination
        v-model="page"
        :length="pageNum"
        prev-icon="fa-caret-left"
        next-icon="fa-caret-right"
      ></v-pagination
    ></v-col>
    <v-row>
      <v-col
        cols="12"
        sm="6"
        v-for="(adapter, index) in displayAdapters"
        :key="index"
      >
        <PublishCard
          :name="adapter.name"
          :desc="adapter.desc"
          :id="adapter.id"
          :author="adapter.author"
          :link="adapter.repo"
        ></PublishCard>
      </v-col>
    </v-row>
    <v-col cols="12">
      <v-pagination
        v-model="page"
        :length="pageNum"
        prev-icon="fa-caret-left"
        next-icon="fa-caret-right"
      ></v-pagination>
    </v-col>
  </v-card>
</template>

<script>
import PublishCard from './PublishCard.vue'
import adapters from '../public/adapters.json'

export default {
  name: 'Adapters',
  components: {
    PublishCard,
  },
  data() {
    return {
      adapters: adapters,
      filterText: '',
      page: 1,
      dialog: false,
      valid: false,
      newAdapter: {
        name: null,
        desc: null,
        id: null,
        link: null,
        repo: null,
      },
    }
  },
  computed: {
    pageNum() {
      return Math.ceil(this.filteredAdapters.length / 10)
    },
    filteredAdapters() {
      return this.adapters.filter((adapter) => {
        return (
          adapter.id.indexOf(this.filterText || '') != -1 ||
          adapter.name.indexOf(this.filterText || '') != -1 ||
          adapter.desc.indexOf(this.filterText || '') != -1 ||
          adapter.author.indexOf(this.filterText || '') != -1
        )
      })
    },
    displayAdapters() {
      return this.filteredAdapters.slice((this.page - 1) * 10, this.page * 10)
    },
    publishPlugin() {
      if (!this.$refs.newAdapterForm.validate()) {
        return
      }
      const title = encodeURIComponent(
        `Adapter: ${this.newAdapter.name}`
      ).replace(/%2B/gi, '+')
      const body = encodeURIComponent(
        `
**协议名称：**

${this.newAdapter.name}

**协议功能：**

${this.newAdapter.desc}

**PyPI 项目名：**

${this.newAdapter.link}

**协议 import 包名：**

${this.newAdapter.id}

**协议项目仓库/主页链接：**

${this.newAdapter.repo}

<!-- DO NOT EDIT ! -->
<!--
- id: ${this.newAdapter.id}
- link: ${this.newAdapter.link}
- name: ${this.newAdapter.name}
- desc: ${this.newAdapter.desc}
- repo: ${this.newAdapter.repo}
-->
`.trim()
      ).replace(/%2B/gi, '+')
      window.open(
        `https://github.com/nonebot/nonebot2/issues/new?title=${title}&body=${body}&labels=Adapter`
      )
    },
  },
}
</script>
