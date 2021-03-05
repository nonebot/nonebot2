<template>
  <v-card flat class="bots">
    <v-row>
      <v-col cols="12" sm="4">
        <v-text-field
          v-model="filterText"
          dense
          rounded
          outlined
          clearable
          hide-details
          label="Filter Bot"
        >
          <template v-slot:prepend-inner>
            <div class="v-input__icon v-input__icon--prepend-inner">
              <v-icon small>fa-filter</v-icon>
            </div>
          </template>
        </v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-dialog v-model="dialog" max-width="600px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn dark block color="primary" v-bind="attrs" v-on="on"
              >Publish Your Bot
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">Bot Information</span>
            </v-card-title>
            <v-card-text>
              <v-form ref="newBotForm" v-model="valid" lazy-validation>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newBot.name"
                        label="机器人名称"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newBot.desc"
                        label="机器人介绍"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newBot.repo"
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
                Close
              </v-btn>
              <v-btn
                :disabled="!valid"
                color="blue darken-1"
                text
                @click="
                  dialog = false;
                  publishBot();
                "
              >
                Publish
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
      <v-col cols="12" sm="4">
        <v-pagination
          v-model="page"
          :length="pageNum"
          prev-icon="fa-caret-left"
          next-icon="fa-caret-right"
        ></v-pagination>
      </v-col>
    </v-row>
    <hr />
    <v-row>
      <v-col cols="12" sm="6" v-for="(bot, index) in displayBots" :key="index">
        <PublishCard
          :name="bot.name"
          :desc="bot.desc"
          :author="bot.author"
          :link="bot.repo"
        ></PublishCard>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-pagination
          v-model="page"
          :length="pageNum"
          prev-icon="fa-caret-left"
          next-icon="fa-caret-right"
        ></v-pagination>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import PublishCard from "./PublishCard.vue";
import bots from "../public/bots.json";

export default {
  name: "Bots",
  components: {
    PublishCard
  },
  data() {
    return {
      bots: bots,
      filterText: "",
      page: 1,
      dialog: false,
      valid: false,
      newBot: {
        name: null,
        desc: null,
        repo: null
      }
    };
  },
  computed: {
    pageNum() {
      return Math.ceil(this.filteredBots.length / 10);
    },
    filteredBots() {
      return this.bots.filter(bot => {
        return (
          bot.id.indexOf(this.filterText || "") != -1 ||
          bot.name.indexOf(this.filterText || "") != -1 ||
          bot.desc.indexOf(this.filterText || "") != -1 ||
          bot.author.indexOf(this.filterText || "") != -1
        );
      });
    },
    displayBots() {
      return this.filteredBots.slice((this.page - 1) * 10, this.page * 10);
    },
    publishBot() {
      if (!this.$refs.newBotForm.validate()) {
        return;
      }
      const title = encodeURIComponent(`Bot: ${this.newBot.name}`).replace(
        /%2B/gi,
        "+"
      );
      const body = encodeURIComponent(
        `
**机器人名称：**

${this.newBot.name}

**机器人功能：**

${this.newBot.desc}

**机器人项目仓库/主页链接：**

${this.newBot.repo}

<!-- DO NOT EDIT ! -->
<!--
- name: ${this.newBot.name}
- desc: ${this.newBot.desc}
- repo: ${this.newBot.repo}
-->
`.trim()
      ).replace(/%2B/gi, "+");
      window.open(
        `https://github.com/nonebot/nonebot2/issues/new?title=${title}&body=${body}&labels=Bot`
      );
    }
  }
};
</script>
