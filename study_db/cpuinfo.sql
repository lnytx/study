/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50703
Source Host           : localhost:3306
Source Database       : get_sysinfo

Target Server Type    : MYSQL
Target Server Version : 50703
File Encoding         : 65001

Date: 2017-06-06 17:05:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `cpuinfo`
-- ----------------------------
DROP TABLE IF EXISTS `cpuinfo`;
CREATE TABLE `cpuinfo` (
  `IP` varchar(20) NOT NULL,
  `hostname` varchar(30) NOT NULL,
  `scputimes` varchar(10) DEFAULT NULL,
  `dpc` varchar(20) DEFAULT NULL,
  `idle` varchar(20) DEFAULT NULL,
  `interrupt` varchar(20) DEFAULT NULL,
  `system` varchar(20) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `iowait` float(20,0) DEFAULT NULL,
  `steal` float(20,0) DEFAULT NULL,
  `irq` float(20,0) DEFAULT NULL,
  `softirq` float(20,0) DEFAULT NULL,
  `guest` float(20,0) DEFAULT NULL,
  `nice` float(20,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of cpuinfo
-- ----------------------------
