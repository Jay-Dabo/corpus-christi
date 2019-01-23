<template>
  <div>
    <v-layout justify-center>
      <v-flex shrink class="mb-2">
        <h1 class="hidden-sm-and-up">{{ $t("translation.header") }}</h1>
      </v-flex>
    </v-layout>
    <v-toolbar class="pa-1" extension-height="64px">
      <v-layout justify-space-between>
        <v-flex shrink align-self-center>
          <v-toolbar-title class="hidden-xs-only">{{
            $t("translation.header")
          }}</v-toolbar-title>
        </v-flex>
        <v-spacer></v-spacer>
        <v-text-field
          class="max-width-250 mr-2"
          v-model="search"
          append-icon="search"
          v-bind:label="$t('actions.search')"
          single-line
          hide-details
        ></v-text-field>
      </v-layout>
      <v-layout row slot="extension" justify-space-between align-center>
        <v-flex>
          <v-select
            class="max-width-250 mr-2"
            prefix="From: "
            hide-details
            solo
            single-line
            :items="localeList"
            v-model="translateFromLocale"
          >
          </v-select>
        </v-flex>
        <v-flex>
          <v-select
            class="max-width-250 mr-2"
            prefix="To: "
            hide-details
            solo
            single-line
            :items="localeList"
            v-model="translateToLocale"
          >
          </v-select>
        </v-flex>
      </v-layout>
    </v-toolbar>
    <v-data-table
      :headers="headers"
      :rows-per-page-items="rowsPerPageItem"
      :items="translations"
      :search="search"
      :loading="tableLoading"
      :pagination.sync="paginationInfo"
      must-sort
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td class="hover-hand">{{ props.item.translateFrom.gloss }}</td>
        <td class="hover-hand">{{ props.item.translateTo.gloss }}</td>
        <td class="hover-hand">
          <template v-if="props.item.translateTo.verified">
            {{ $t("translation.verified") }}
          </template>
          <template v-else>
            <v-tooltip bottom v-if="!props.item.translateTo.verified">
              <v-btn
                icon
                outline
                small
                color="primary"
                slot="activator"
                v-on:click="verify(props.item.translateTo)"
                :loading="!props.item.translateTo"
              >
                <v-icon small>undo</v-icon>
              </v-btn>
              <span>{{ $t("translation.verify") }}</span>
            </v-tooltip>
          </template>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "TranslationTable",
  data() {
    return {
      translateFromLocale: null,
      translateToLocale: null,
      localeList: [],
      translations: [],
      search: "",
      rowsPerPageItem: [
        10,
        15,
        25,
        { text: "$vuetify.dataIterator.rowsPerPageAll", value: -1 }
      ],
      paginationInfo: {
        sortBy: "translateTo", //default sorted column
        rowsPerPage: 10,
        page: 1
      },
      tableLoading: true,
      fromTranslations: null,
      toTranslations: null
    };
  },
  computed: {
    headers() {
      this.getLocales();
      return [
        {
          text: this.$t("translation." + this.translateFromLocale),
          value: "translateFrom"
        },
        {
          text: this.$t("translation." + this.translateToLocale),
          value: "translateTo"
        },
        { text: this.$t("translation.verified"), value: "translateTo.verified" }
      ];
    },
    ...mapGetters(["currentLanguageCode"])
  },
  methods: {
    verify(localeValue) {
      console.log("verify", localeValue);
      // TODO: Patch item to have `verified=true`
    },
    getLocales() {
      this.$http
        .get(`/api/v1/i18n/locales`)
        .then(resp => {
          this.localeList = [];
          resp.data.forEach(locale => {
            this.localeList.push({
              text: locale.desc,
              value: locale.code
            });
          });
          if (!this.translateFromLocale) {
            this.translateFromLocale = this.localeList[0].value;
          }
          if (!this.translateToLocale) {
            this.translateToLocale = this.localeList[1].value;
          }
          this.updateData();
        })
        .catch(err => {
          console.error(err.response);
        });
    },
    updateData() {
      this.tableLoading = true;
      this.$http
        .get(`/api/v1/i18n/values/${this.translateFromLocale}`)
        .then(resp => {
          this.fromTranslations = resp.data;
          if (this.toTranslations) {
            this.updatedAllData();
          }
        })
        .catch(err => {
          console.error(err.response);
        });

      this.$http
        .get(`/api/v1/i18n/values/${this.translateToLocale}`)
        .then(resp => {
          this.toTranslations = resp.data;
          if (this.fromTranslations) {
            this.updatedAllData();
          }
        })
        .catch(err => {
          console.error(err.response);
        });
    },
    updatedAllData() {
      this.translations = [];
      this.fromTranslations.forEach(fromTranslation => {
        let toTranslationList = this.toTranslations.filter(
          tr => tr.key_id === fromTranslation.key_id
        );
        var toTranslation = {
          gloss: this.$t("translation.no-translation"),
          verified: false
        };
        if (toTranslationList.length > 0) {
          toTranslation = toTranslationList[0];
        }
        this.translations.push({
          translateFrom: fromTranslation,
          translateTo: toTranslation
        });
      });
      this.tableLoading = false;
    }
  }
};
</script>
