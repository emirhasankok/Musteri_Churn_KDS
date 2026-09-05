using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Churn.Migrations
{
    /// <inheritdoc />
    public partial class @new : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Musteriler",
                columns: table => new
                {
                    Musteri_ID = table.Column<int>(type: "int", nullable: false),
                    Yas = table.Column<int>(type: "int", nullable: false),
                    Kullanim_Suresi_Ay = table.Column<int>(type: "int", nullable: false),
                    Aylik_Harcama_TL = table.Column<decimal>(type: "decimal(10,2)", nullable: false),
                    Destek_Talebi_Sayisi = table.Column<int>(type: "int", nullable: true, defaultValue: 0),
                    Son_Giris_Gunu = table.Column<int>(type: "int", nullable: false),
                    Churn_Durumu = table.Column<bool>(type: "bit", nullable: true, defaultValue: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__Musteril__1E6CEE0AE1097A5D", x => x.Musteri_ID);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Musteriler");
        }
    }
}
