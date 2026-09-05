using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace Churn.Models;

public partial class ChurnCrmDbContext : DbContext
{
    public ChurnCrmDbContext()
    {
    }

    public ChurnCrmDbContext(DbContextOptions<ChurnCrmDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Musteriler> Musterilers { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
        => optionsBuilder.UseSqlServer("Server=EMRH;Database=ChurnCRM_DB;Trusted_Connection=True;TrustServerCertificate=True;");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Musteriler>(entity =>
        {
            entity.HasKey(e => e.MusteriId).HasName("PK__Musteril__1E6CEE0AE1097A5D");

            entity.ToTable("Musteriler");

            entity.Property(e => e.MusteriId)
                .ValueGeneratedNever()
                .HasColumnName("Musteri_ID");
            entity.Property(e => e.AylikHarcamaTl)
                .HasColumnType("decimal(10, 2)")
                .HasColumnName("Aylik_Harcama_TL");
            entity.Property(e => e.ChurnDurumu)
                .HasDefaultValue(false)
                .HasColumnName("Churn_Durumu");
            entity.Property(e => e.DestekTalebiSayisi)
                .HasDefaultValue(0)
                .HasColumnName("Destek_Talebi_Sayisi");
            entity.Property(e => e.KullanimSuresiAy).HasColumnName("Kullanim_Suresi_Ay");
            entity.Property(e => e.SonGirisGunu).HasColumnName("Son_Giris_Gunu");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
